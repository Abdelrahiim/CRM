from team.models import Team
from django.db.models import Q



def active_team(request):
    if request.user.is_authenticated:
        active_team = Team.objects.filter(Q(created_by=request.user)|Q(members__id = request.user.id)).first()
    else :
        active_team= None
    return {'active_team':active_team}