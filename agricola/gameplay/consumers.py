import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from .serializer import *
from random import shuffle, choice

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        request_type = text_data_json.get('type')

        if request_type == 'get_account_data':
            card_data = await self.get_card_data()
            await self.send_json(card_data)

        if request_type == 'choose_first_player':
            fst_player = await self.choose_first_player()
            await self.send_json(fst_player)

        if request_type == 'get_random_subfacilitycards':
            random_cards = await self.get_random_subfacilitycards()
            await self.send_json(random_cards)

        if request_type == 'get_random_jobcards':
            random_cards = await self.get_random_jobcards()
            await self.send_json(random_cards)

        if request_type == 'get_turn':
            await self.get_turn()

        if request_type == 'take_action':
            await self.take_action(text_data_json)

    async def choose_first_player(self):
        players = Player.objects.all()

        if players.exists():
            first_player = choice(players)
            players.update(fst_player=False)
            first_player.fst_player = True
            first_player.save()

            serializer = PlayerSerializer(first_player)
            return serializer.data
        else:
            return "No players found."

    async def get_random_subfacilitycards(self):
        subfacilitycards = list(SubFacilityCard.objects.all())
        shuffle(subfacilitycards)  # 리스트를 랜덤하게 섞습니다.

        chunked_subcards = [subfacilitycards[i:i + 7] for i in range(0, 14, 7)]  # 7개씩 두 묶음으로 나눕니다.
        serialized_data = []

        for chunk in chunked_subcards:
            serializer = SubFacilityCardSerializer(chunk, many=True)
            serialized_data.append(serializer.data)

        return serialized_data

    async def get_random_jobcards(self):
        jobcards = list(JobCard.objects.all())
        shuffle(jobcards)  # 리스트를 랜덤하게 섞습니다.

        chunked_subcards = [jobcards[i:i + 7] for i in range(0, 14, 7)]  # 7개씩 두 묶음으로 나눕니다.
        serialized_data = []

        for chunk in chunked_subcards:
            serializer = JobCardSerializer(chunk, many=True)
            serialized_data.append(serializer.data)

        return serialized_data

    async def get_turn(self):
        game_status = self.get_queryset().first()  # Assuming there is only one GameStatus instance
        turn_counter = game_status.turn
        await self.send_json({'turn': turn_counter})

    async def take_action(self, data):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        player_id = data.get('player')
        action_id = data.get('action')

        player = Player.objects.get(id=player_id)
        action = ActionBox.objects.get(id=action_id)

        game_status = GameStatus.objects.first()
        turn_counter = game_status.turn

        is_first_player_turn = turn_counter % 2 == 1

        if (is_first_player_turn and player.is_first_player) or (
                not is_first_player_turn and not player.is_first_player):
            if action_id == 1:
                # perform_action_1()
                pass
            elif action_id == 2:
                # perform_action_2()
                pass

            game_status.turn = turn_counter + 1
            game_status.save()

            new_instance = FamilyPosition.objects.create(player=player, action=action, turn=turn_counter + 1)
            new_instance.save()

            response_data = serializer.data
        else:
            response_data = {'error': 'It is not your turn to take an action.'}

        await self.send_json(response_data)