from flask import Blueprint, render_template, jsonify, request
from app.services.agidesk_service import AgideskService
from datetime import datetime, timedelta
from functools import lru_cache

bp = Blueprint('main', __name__)
agidesk_service = AgideskService()

def process_ticket(ticket: dict) -> dict:
    """Processa um único ticket para exibição"""
    try:
        created_at = datetime.strptime(ticket['created_at'], '%Y-%m-%d %H:%M:%S')
        
        # Adiciona informações formatadas
        return {
            'id': ticket.get('id'),
            'display_title': f"{ticket.get('prefix', '')}{ticket.get('id', '')} - {ticket.get('title', 'Sem título')}",
            'status_id': ticket.get('status_id'),
            'status_color': {
                '1': 'warning',    # Aberto
                '2': 'primary',    # Em andamento
                '3': 'success',    # Resolvido
                '4': 'secondary'   # Fechado
            }.get(str(ticket.get('status_id')), 'info'),
            'responsible': ticket.get('responsible_id'),
            'created_at': created_at.strftime('%d/%m/%Y %H:%M'),
            'time_open': calculate_time_open(created_at),
            'team_name': ticket.get('team', {}).get('title', 'Sem equipe')
        }
    except Exception as e:
        print(f"Erro ao processar ticket {ticket.get('id')}: {str(e)}")
        return {
            'id': ticket.get('id'),
            'display_title': ticket.get('title', 'Sem título'),
            'status_id': '0',
            'status_color': 'secondary',
            'responsible': None,
            'created_at': 'Data desconhecida',
            'time_open': 'Tempo desconhecido',
            'team_name': 'Sem equipe'
        }

def calculate_time_open(created_at: datetime) -> str:
    """Calcula o tempo que o ticket está aberto"""
    time_open = datetime.now() - created_at
    if time_open.days > 0:
        return f"{time_open.days} dias"
    hours = time_open.seconds // 3600
    if hours > 0:
        return f"{hours} horas"
    return "Menos de 1 hora"

@lru_cache(maxsize=1)
def get_responsibles():
    """Cache da lista de responsáveis"""
    tickets = agidesk_service.get_all_tickets()
    responsibles = set()
    
    for ticket in tickets:
        if 'followers' in ticket:
            for follower in ticket['followers']:
                if follower.get('id') and follower.get('title'):
                    responsibles.add((follower['id'], follower['title']))
    
    return [{'id': r[0], 'name': r[1]} for r in sorted(responsibles, key=lambda x: x[1])]

@bp.route('/')
def index():
    """Rota principal que exibe o dashboard"""
    with_responsible, without_responsible = agidesk_service.get_tickets_count()
    total_tickets = with_responsible + without_responsible
    
    # Conta chamados abertos hoje
    all_tickets = agidesk_service.get_all_tickets()
    today = datetime.now().date()
    today_tickets = sum(1 for ticket in all_tickets 
                       if datetime.strptime(ticket['created_at'].split()[0], '%Y-%m-%d').date() == today)
    
    return render_template('index.html',
                         with_responsible=with_responsible,
                         without_responsible=without_responsible,
                         total_tickets=total_tickets,
                         today_tickets=today_tickets)

@bp.route('/chamados')
def chamados():
    """Rota que lista todos os chamados"""
    tickets = [process_ticket(ticket) for ticket in agidesk_service.get_all_tickets()]
    return render_template('chamados.html',
                         tickets=tickets,
                         responsibles=get_responsibles())

@bp.route('/filtros')
def filtros():
    """Rota para a página de filtros avançados"""
    return render_template('filtros.html',
                         responsibles=get_responsibles())

@bp.route('/api/tickets/filter', methods=['POST'])
def filter_tickets():
    """API endpoint para filtrar chamados"""
    filters = request.get_json()
    
    tickets = agidesk_service.get_all_tickets()
    filtered_tickets = []
    
    for ticket in tickets:
        # Aplica os filtros
        if matches_filters(ticket, filters):
            filtered_tickets.append(ticket)
    
    return jsonify(filtered_tickets)

@bp.route('/api/ticket/<int:ticket_id>')
def get_ticket(ticket_id):
    """API endpoint para obter detalhes de um chamado específico"""
    tickets = agidesk_service.get_all_tickets()
    ticket = next((t for t in tickets if t['id'] == ticket_id), None)
    
    if ticket:
        return jsonify(ticket)
    return jsonify({'error': 'Chamado não encontrado'}), 404

# Adiciona um endpoint para atualização manual do cache
@bp.route('/api/refresh-cache', methods=['POST'])
def refresh_cache():
    """Força a atualização do cache"""
    agidesk_service.clear_cache()
    get_responsibles.cache_clear()
    return jsonify({'status': 'success', 'message': 'Cache atualizado com sucesso'})

def matches_filters(ticket, filters):
    """Função auxiliar para verificar se um ticket corresponde aos filtros"""
    if filters.get('start_date'):
        ticket_date = datetime.strptime(ticket['created_at'].split()[0], '%Y-%m-%d')
        start_date = datetime.strptime(filters['start_date'], '%Y-%m-%d')
        if ticket_date < start_date:
            return False
            
    if filters.get('end_date'):
        ticket_date = datetime.strptime(ticket['created_at'].split()[0], '%Y-%m-%d')
        end_date = datetime.strptime(filters['end_date'], '%Y-%m-%d')
        if ticket_date > end_date:
            return False
    
    if filters.get('status') and ticket['status'] not in filters['status']:
        return False
        
    if filters.get('responsible_ids') and ticket.get('responsible_id') not in filters['responsible_ids']:
        return False
        
    if filters.get('priority') and ticket.get('priority') != filters['priority']:
        return False
        
    return True