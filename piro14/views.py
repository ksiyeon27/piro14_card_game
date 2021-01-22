from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from .models import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
import random
from django.db.models.query import Q
from .forms import GameForm

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)

        social_app_name = sociallogin.account.provider.upper()

        if social_app_name == "GOOGLE":
            User.objects.get_or_create_google_user(user_pk=user.pk, user_email=user.email, user_name=user.name)

#(1번)
def main_before(request):
    user = User.objects.all()

    return render(request, 'piro14/main_bflog.html', {
        'user': user,
    })

#(2번)
def main_after(request):
    user = User.objects.all()
    return render(request, 'piro14/main_aflog.html', {
        'user': user,
    })
#메인 완성쪽


# 게임 목록(4번)
def game_list(request):
    user=request.user
    games = Game.objects.filter(Q(creator=user)|Q(opponent=user))
    ctx = {
           'games' : games
           }
    return render(request,'piro14/game_list.html', ctx) # 리스트 템플릿 경로와 매핑
    
# 게임 삭제
def game_delete(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        game.delete()
        return redirect('piro14:game_list.html') # 게임 리스트로 이동
    else:
        return redirect('piro14:game_list.html') # 게임 리스트로 이동

# 세부내역(5번)
def game_detail(request, pk):
    user = request.user
    game = Game.objects.get(id=pk)
    ctx = {
        'game':game,
        'user':user,
    }
    return render(request, 'piro14/game_detail.html', ctx ) #세부내역 템플릿 경로 매핑

# 랭킹(7번)
def game_ranking(request):
    users = User.objects.all().order_by('-score') #유저매니저 클래스에 score 객체 추가할 시 
    ctx = {
        'users':users,
    }
    return render(request, 'piro14/game_ranking.html', ctx )#랭킹 템플릿 경로 매핑


#공격(3번)
#장고 폼버전
# def game_attack(request):
#     if request.method == "POST": #post방식
#         # form = GameForm(request.POST)
#         # if form.is_valid():
#         data = request.POST
#         creator = request.user
#         opponent = User.objects.get(username=data.get('opponent')
#         creator_card = int(data.get('creator_card'))
#         current_turn = opponent

#         game = Game()
#         game.creator = creator
#         game.opponent = opponent
#         game.creator_card = creator_card
#         game.current_turn = current_turn
#         game.save()

#         return redirect('piro14/game_detail.html', pk=game.id) # 공격 템플릿 매핑
#     else:
#         form = GameForm() #get방식
#         ctx={"form": form}
#         return render(request, "piro14/game_form.html", ctx)

def game_attack(request):
    if request.method == 'POST': # POST 형식으로 폼에 입력받은 값을 서버에 요청할 경우
        data = request.POST
        creator = request.user
        opponent = User.objects.get(username=data.get('opponent'))
        creator_card = int(data.get('creator_card'))
        current_turn = opponent

        game = Game()
        game.creator = creator
        game.opponent = opponent
        game.creator_card = creator_card
        game.current_turn = current_turn
        game.greater = random.choice([True, False])
        game.save()

        return redirect('piro14:game_detail', pk=game.id)

    else:
        creator = request.user
        opponent_options = User.objects.exclude(id=creator.id) #pk를 제외한 나머지
        creator_card_options = random.sample(range(1,11), 5)#1~10의 정수중 5개 뽑아서 리스트 생성
        # 클래스의 객체들을 넣고
        ctx = {
            'creator' : creator,
            'opponent_options' : opponent_options,
            'creator_card_options' : creator_card_options
        }
        return render(request, 'piro14/game_attack.html', ctx )
    # 각각의 객체들을 ctx에 넣고
    # 공격 템플릿과 매핑함

#반격(6번) - 구현 필요
def game_counter_attack(request, pk):
    if request.method == 'POST': # POST 형식으로 폼에 입력받은 값을 서버에 요청할 경우
        game = Game.objects.get(id=pk)
        data = request.POST
        game.opponent_card = int(data.get('opponent_card'))
        game.current_turn = game.creator
        

        game_creator = Profile.objects.get(user=game.creator)
        game_opponent = Profile.objects.get(user=game.opponent)

        if game.greater == True and game.creator_card > game.opponent_card:
            game.winner = game.creator
            game.loser = game.opponent
            game_creator.score += game.creator_card
            game_opponent.score -= game.opponent_card
        elif game.greater == True and game.creator_card < game.opponent_card: 
            game.winner = game.opponent
            game.loser = game.creator
            game_creator.score -= game.creator_card
            game_opponent.score += game.opponent_card
        elif game.greater == False and game.creator_card > game.opponent_card:
            game.winner = game.opponent
            game.loser = game.creator
            game_creator.score -= game.creator_card
            game_opponent.score += game.opponent_card
        elif game.greater == False and game.creator_card < game.opponent_card: 
            game.winner = game.creator
            game.loser = game.opponent
            game_creator.score += game.creator_card
            game_opponent.score -= game.opponent_card
        else: 
            game.draw = True
            game_creator.score += game.creator_card
            game_opponent.score += game.opponent_card
            
        game.completed = True
        return redirect('piro14:game_detail', pk=game.id)
    
    else:
        game = Game.objects.get(id=pk)
        creator = game.creator
        opponent_card_options = random.sample(range(1,11), 5)#1~10의 정수중 5개 뽑아서 리스트 생성
        # 클래스의 객체들을 넣고
        ctx = {
            'opponent_card_options' : opponent_card_options,
            'creator' : creator
        }
        return render(request, 'piro14/game_counter_attack.html', ctx )