from django.contrib.auth.models import Group, User
from rest_framework import serializers
from . import models, fields
from api.models import unique_individual_group, InteractionStatistic, Adaptative, Badge, Challenge, DevelopmentTool, EasterEgg, Gift, GiftOpener, KnowledgeShare, Level, Lottery, Point, SocialNetwork, SocialStatus, Unlockable, Leaderboard, Gamer, GComponent, GMechanic, GMechanicList,GamerProfile, EmotionProfile, SocialProfile
from api.models import AdaptativeWidget, BadgeWidget, ChallengeWidget, DevelopmentToolWidget, EasterEggWidget, GiftWidget, GiftOpenerWidget, KnowledgeShareWidget, LevelWidget, LotteryWidget, PointWidget, SocialNetworkWidget, SocialStatusWidget, UnlockableWidget, LeaderboardWidget
from rest_framework.response import Response
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.utils import IntegrityError
from django.http import Http404
from django.template.response import TemplateResponse
from drf_enum_field.serializers import EnumFieldSerializerMixin
from rest_framework.exceptions import ValidationError

import threading
lock = threading.Lock()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id','username','email', 'groups']
        read_only_fields = ('groups',)
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()]
            }   
        }
        #read_only_fields = ('groups')

class EmotionProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EmotionProfile
        fields = ['url', 'valence','arousal']


class GamerProfileSerializer(serializers.HyperlinkedModelSerializer):
    data = fields.JSONSerializerField()
    class Meta:
        model = GamerProfile
        fields = ['url', 'disruptor','free_spirit', 'achiever','player','socializer','philantropist', 'no_player','data']

class SocialProfileSerializer(serializers.HyperlinkedModelSerializer):
    data = fields.JSONSerializerField()
    image = fields.EnumField(enum=models.SocialProfile.AvatarType)
    class Meta:
        model = SocialProfile
        fields = ['url', 'image', 'description','data']

class GamerSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    gamer_profile = GamerProfileSerializer()
    emotion_profile = EmotionProfileSerializer()
    social_profile = SocialProfileSerializer()
    
    class Meta:
        model = Gamer
        fields = ['url','user','social_profile','gamer_profile','emotion_profile']

    def create(self, validated_data):
        #try:
        user_data = validated_data.pop('user')

       
        #print(user_data)
        try:
            individual_group = Group.objects.create(name = 'individual_' + user_data['username'])
        #print(user_data)
            user_data['groups'] += [individual_group]
        except: pass
        user = UserSerializer.create(UserSerializer(),validated_data=user_data)
        
        #user.set_password(validated_data.get('username'))
        user.save()
        #print(validated_data)

        gamer_profile_data = validated_data.pop('gamer_profile')
        emotion_profile_data = validated_data.pop('emotion_profile')
        social_profile_data = validated_data.pop('social_profile')

        if 'disruptor' in gamer_profile_data.keys(): disruptor_data = gamer_profile_data['disruptor']
        else: disruptor_data = 1
        if 'free_spirit' in gamer_profile_data.keys(): free_spirit_data = gamer_profile_data['free_spirit']
        else: free_spirit_data = 1
        if 'achiever' in gamer_profile_data.keys(): achiever_data = gamer_profile_data['achiever']
        else: achiever_data = 1
        if 'player' in gamer_profile_data.keys(): player_data = gamer_profile_data['player']
        else: player_data = 1
        if 'socializer' in gamer_profile_data.keys(): socializer_data = gamer_profile_data['socializer']
        else: socializer_data = 1
        if 'philantropist' in gamer_profile_data.keys(): philantropist_data = gamer_profile_data['philantropist']
        else: philantropist_data = 1
        if 'no_player' in gamer_profile_data.keys(): no_player_data = gamer_profile_data['no_player']
        else: no_player_data = 0
        if 'data' in gamer_profile_data.keys(): 
            if gamer_profile_data['data']:
                data_data = gamer_profile_data['data']
            else: data_data = {"level":0,"score":0,"$":0,"badges":[],"unlockables":[],"challenges":[], "gifts" : []}
        else: data_data = {"level":0,"score":0,"$":0,"badges":[],"unlockables":[],"challenges":[], "gifts" : []}
        
        gprofile = GamerProfile.objects.create(disruptor = disruptor_data,
                                                free_spirit =  free_spirit_data,
                                                achiever =  achiever_data,
                                                player =  player_data,
                                                socializer =  socializer_data,
                                                philantropist =  philantropist_data,
                                                no_player =  no_player_data,
                                                data = data_data)

        if 'valence' in emotion_profile_data.keys(): valence_data = emotion_profile_data['valence']
        else: valence_data = 0
        if 'arousal' in emotion_profile_data.keys(): arousal_data = emotion_profile_data['arousal']
        else: arousal_data = 1
        
        eprofile = EmotionProfile.objects.create(valence = valence_data,
                                                arousal =  arousal_data)


        if 'image' in social_profile_data.keys():
            image_data = social_profile_data['image']
        else:
            image_data = "diamond"
        sprofile = SocialProfile.objects.create(image = image_data,data = {"friends":[],"followers":0, "views":0})
        
        gamer = Gamer.objects.create(user = user, 
                                    emotion_profile = eprofile,
                                    gamer_profile = gprofile,
                                    social_profile = sprofile
                                    ) 
        return gamer
        
        # except IntegrityError as error:
        #     print(error)
        #     print("Error creating user: The selected username alredy exists")
        #     return Gamer()
   
    def update(self, instance, validated_data):
        val = validated_data.get('user')['username']
        if 'groups' in validated_data.get('user'):
            grps = validated_data.get('user')['groups']
            instance.user.groups.set(grps)
        User.objects.filter(username=instance.user.username).update(username=val,email = validated_data.get('user')['email'])
        instance.refresh_from_db()
       
        gamer_profile_data = validated_data.pop('gamer_profile')
        emotion_profile_data = validated_data.pop('emotion_profile')
        social_profile_data = validated_data.pop('social_profile')

        if 'disruptor' in gamer_profile_data.keys(): disruptor_data = gamer_profile_data['disruptor']
        else: disruptor_data = instance.gamer_profile.disruptor
        if 'free_spirit' in gamer_profile_data.keys(): free_spirit_data = gamer_profile_data['free_spirit']
        else: free_spirit_data = instance.gamer_profile.free_spirit
        if 'achiever' in gamer_profile_data.keys(): achiever_data = gamer_profile_data['achiever']
        else: achiever_data = instance.gamer_profile.achiever
        if 'player' in gamer_profile_data.keys(): player_data = gamer_profile_data['player']
        else: player_data = instance.gamer_profile.player
        if 'socializer' in gamer_profile_data.keys(): socializer_data = gamer_profile_data['socializer']
        else: socializer_data = instance.gamer_profile.socializer
        if 'philantropist' in gamer_profile_data.keys(): philantropist_data = gamer_profile_data['philantropist']
        else: philantropist_data = instance.gamer_profile.philantropist
        if 'no_player' in gamer_profile_data.keys(): no_player_data = gamer_profile_data['no_player']
        else: no_player_data = instance.gamer_profile.no_player
        if 'data' in gamer_profile_data.keys(): data_data = gamer_profile_data['data']
        else: data_data = instance.gamer_profile.data 

        # The following code add an attribute to gamer_profile.data when a created user updates its profile. Use it carefully!
        # Can be used in a similar fashion to update social_profile.data
        # if 'gifts' not in data_data.keys():
        #     data_data['gifts'] = []

        instance.gamer_profile.disruptor = disruptor_data
        instance.gamer_profile.free_spirit = free_spirit_data
        instance.gamer_profile.achiever = achiever_data
        instance.gamer_profile.player = player_data
        instance.gamer_profile.socializer = socializer_data
        instance.gamer_profile.philantropist = philantropist_data
        instance.gamer_profile.no_player = no_player_data
        instance.gamer_profile.data = data_data
        instance.gamer_profile.save()  

        if 'valence' in emotion_profile_data.keys(): valence_data = emotion_profile_data['valence']
        else: valence_data = instance.emotion_profile.valence
        if 'arousal' in emotion_profile_data.keys(): arousal_data = emotion_profile_data['arousal']
        else: arousal_data = instance.emotion_profile.arousal
        
        instance.emotion_profile.valence = valence_data
        instance.emotion_profile.arousal = arousal_data
        instance.emotion_profile.save()

        if 'image' in social_profile_data.keys(): image_data = social_profile_data['image']
        else: image_data = instance.social_profile.image
        if 'description' in social_profile_data.keys(): description_data = social_profile_data['description']
        else: description_data = instance.social_profile.description
        if 'data' in social_profile_data.keys(): data_data = social_profile_data['data']
        else: data_data = instance.social_profile.data

        instance.social_profile.description = description_data
        instance.social_profile.image = image_data
        instance.social_profile.data = data_data
        instance.social_profile.save()  
    
        instance.save()
        return instance

class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ['url', 'name']

class InteractionStatisticSerializer(serializers.HyperlinkedModelSerializer):
    #userid = GamerSerializer().Meta.fields
    #mechanic = serializers.SerializerMethodField(read_only = False)
    #user = GamerSerializer()
    #user = serializers.SerializerMethodField()
    log = fields.JSONSerializerField(read_only = True)

    def get_user(self, obj):
        # obj is model instance
        return obj.user.user.UnicodeUsernameValidator
    
    def get_mechanic(self, obj):
        # obj is model instance
        return obj.mechanic.id
        
    class Meta:
        model = InteractionStatistic
        fields = ['url', 'id','mechanic','user', 'log','interaction_index']
        ordering = ['-id']
        #read_only_fields =
             
        
class GMechanicSerializer(EnumFieldSerializerMixin,serializers.HyperlinkedModelSerializer):
    mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    
    #statistics = InteractionStatisticSerializer(many = True, read_only = True)
    class Meta:
        model = GMechanic
        fields = ['url','id','title','mechanic_type','html']
        read_only_fields = ('html',)
        depth = 2

    def create(self, validated_data):
        # create default gmechanic instance
        lock.acquire()
        try:
            instance = super().create(validated_data)
            # Create default statistics for all users 
            return instance
        except:
            lock.release()
            raise Http404
        
class GMechanicListSerializer(GMechanicSerializer):
    mechanic = fields.EnumField(enum=models.GMechanicList.Mechanics)
    
    #statistics = InteractionStatisticSerializer(many = True, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = GMechanicList
        fields = GMechanicSerializer.Meta.fields[:3] + ['mechanic'] +  GMechanicSerializer.Meta.fields[3:]

    def create(self, validated_data):
        # create default gmechanic instance
   
        instance = super().create(validated_data)
        instance.mechanic_type = GMechanic.MechanicType.Change
        instance.save()
        # Create default statistics for all users 
        return instance
  


class DevelopmentToolSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    mechanic_class = fields.EnumField(enum=models.DevelopmentTool.Mechanic)
    class Meta(GMechanicSerializer.Meta):
        model = DevelopmentTool
        fields = GMechanicSerializer.Meta.fields[:3] + ['mechanic_class','attempts'] +  GMechanicSerializer.Meta.fields[3:]

class ChallengeSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = Challenge
        fields = GMechanicSerializer.Meta.fields[:3] + ['icon','name','state','by', 'threshold'] +  GMechanicSerializer.Meta.fields[3:]
        read_only_fields = ('state','html','statistics')
        
class EasterEggSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = EasterEgg
        fields = GMechanicSerializer.Meta.fields[:3] + ['feedback','egg_html'] +  GMechanicSerializer.Meta.fields[3:]
   
class UnlockableSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = Unlockable
        fields = GMechanicSerializer.Meta.fields[:3] + ['icon','name','state','by', 'threshold','locked_html'] +  GMechanicSerializer.Meta.fields[3:]
        read_only_fields = ('state','html','statistics')
        
class BadgeSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = Badge
        fields = GMechanicSerializer.Meta.fields[:3] + ['icon','name','state','by', 'threshold'] +  GMechanicSerializer.Meta.fields[3:]
        read_only_fields = ('state','html','statistics')
   
class LevelSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = Level
        fields = GMechanicSerializer.Meta.fields[:3] + ['value','max_value','by'] +  GMechanicSerializer.Meta.fields[3:]
   
class PointSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = Point
        fields = GMechanicSerializer.Meta.fields[:3] + ['user','score','given_by'] +  GMechanicSerializer.Meta.fields[3:]

class LeaderboardSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    leadders = fields.JSONSerializerField(read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = Leaderboard
        fields = GMechanicSerializer.Meta.fields[:3] + ['length','leadders','sort_by'] +  GMechanicSerializer.Meta.fields[3:]
        #read_only_fields = ('leadders',)
   
class LotterySerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = Lottery
        fields = GMechanicSerializer.Meta.fields[:3] + ['items','by'] +  GMechanicSerializer.Meta.fields[3:]
   
class SocialNetworkSerializer(GMechanicSerializer):
    messages = fields.JSONSerializerField(read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = SocialNetwork
        fields = GMechanicSerializer.Meta.fields[:3] + ['messages'] +  GMechanicSerializer.Meta.fields[3:]
   
class SocialStatusSerializer(GMechanicSerializer):
    competitiveness = fields.EnumField(enum=models.SocialStatus.CompetitionLevel)
    class Meta(GMechanicSerializer.Meta):
        model = SocialStatus
        fields = GMechanicSerializer.Meta.fields[:3] + ['competitiveness'] +  GMechanicSerializer.Meta.fields[3:]
   
class KnowledgeShareSerializer(GMechanicSerializer):
    messages = fields.JSONSerializerField()
    class Meta(GMechanicSerializer.Meta):
        model = KnowledgeShare
        fields = GMechanicSerializer.Meta.fields[:3] + ['messages'] +  GMechanicSerializer.Meta.fields[3:]
   
class GiftSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = Gift
        fields = GMechanicSerializer.Meta.fields[:3] + [] +  GMechanicSerializer.Meta.fields[3:]

class GiftOpenerSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = GiftOpener
        fields = GMechanicSerializer.Meta.fields[:3] + [] +  GMechanicSerializer.Meta.fields[3:]

class AdaptativeSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = Adaptative
        fields = GMechanicSerializer.Meta.fields

#GWidget serializers ----------------------------------------------------------------------------------------

class DevelopmentToolWidgetSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    
    class Meta(GMechanicSerializer.Meta):
        model = DevelopmentToolWidget
        fields = GMechanicSerializer.Meta.fields[:3] + [] +  GMechanicSerializer.Meta.fields[3:]

class ChallengeWidgetSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = ChallengeWidget
        fields = GMechanicSerializer.Meta.fields[:3] + [] +  GMechanicSerializer.Meta.fields[3:]
        #read_only_fields = ('state','html','statistics')
        
class EasterEggWidgetSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = EasterEggWidget
        fields = GMechanicSerializer.Meta.fields[:3] + [] +  GMechanicSerializer.Meta.fields[3:]
   
class UnlockableWidgetSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = UnlockableWidget
        fields = GMechanicSerializer.Meta.fields[:3] + [] +  GMechanicSerializer.Meta.fields[3:]
        #read_only_fields = ('state','html','statistics')
        
class BadgeWidgetSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = BadgeWidget
        fields = GMechanicSerializer.Meta.fields[:3] + [] +  GMechanicSerializer.Meta.fields[3:]
        #read_only_fields = ('state','html','statistics')
   
class LevelWidgetSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = LevelWidget
        fields = GMechanicSerializer.Meta.fields[:3] + [] +  GMechanicSerializer.Meta.fields[3:]
   
class PointWidgetSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = PointWidget
        fields = GMechanicSerializer.Meta.fields[:3] + [] +  GMechanicSerializer.Meta.fields[3:]

class LeaderboardWidgetSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    #leadders = fields.JSONSerializerField(read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = LeaderboardWidget
        fields = GMechanicSerializer.Meta.fields[:3] + [] +  GMechanicSerializer.Meta.fields[3:]
        #read_only_fields = ('leadders',)
   
class LotteryWidgetSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = LotteryWidget
        fields = GMechanicSerializer.Meta.fields[:3] + [] +  GMechanicSerializer.Meta.fields[3:]
   
class SocialNetworkWidgetSerializer(GMechanicSerializer):
    #messages = fields.JSONSerializerField(read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = SocialNetworkWidget
        fields = GMechanicSerializer.Meta.fields[:3] + [] +  GMechanicSerializer.Meta.fields[3:]
   
class SocialStatusWidgetSerializer(GMechanicSerializer):
    #competitiveness = fields.EnumField(enum=models.SocialStatus.CompetitionLevel)
    class Meta(GMechanicSerializer.Meta):
        model = SocialStatusWidget
        fields = GMechanicSerializer.Meta.fields[:3] + [] +  GMechanicSerializer.Meta.fields[3:]
   
class KnowledgeShareWidgetSerializer(GMechanicSerializer):
    #messages = fields.JSONSerializerField()
    class Meta(GMechanicSerializer.Meta):
        model = KnowledgeShareWidget
        fields = GMechanicSerializer.Meta.fields[:3] + [] +  GMechanicSerializer.Meta.fields[3:]
   
class GiftWidgetSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = GiftWidget
        fields = GMechanicSerializer.Meta.fields[:3] + [] +  GMechanicSerializer.Meta.fields[3:]

class GiftOpenerWidgetSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = GiftOpenerWidget
        fields = GMechanicSerializer.Meta.fields[:3] + [] +  GMechanicSerializer.Meta.fields[3:]

class AdaptativeWidgetSerializer(GMechanicSerializer):
    #mechanic_type = fields.EnumField(enum=models.GMechanic.MechanicType, read_only = True)
    class Meta(GMechanicSerializer.Meta):
        model = AdaptativeWidget
        fields = GMechanicSerializer.Meta.fields


class GComponentSerializer(EnumFieldSerializerMixin,serializers.HyperlinkedModelSerializer):
    
    component_type = fields.EnumField(enum=models.GComponent.ComponentType)
    class Meta:
        model = GComponent
        fields = ['url', 'link','mechanics','interacting_users','component_type']

    
