from ..kernel import core
from ..kernel.core import VSkillModifier as V
from ..character import characterKernel as ck
from functools import partial
from ..status.ability import Ability_tool
from . import globalSkill
######   Passive Skill   ######


class JobGenerator(ck.JobGenerator):
    def __init__(self):
        super(JobGenerator, self).__init__()
        self.buffrem = False
        self.jobtype = "str"
        self.vEnhanceNum = 15
        self.preEmptiveSkills = 1
        
        self.ability_list = Ability_tool.get_ability_set('boss_pdamage', 'reuse', 'mess')
    
    def get_modifier_optimization_hint(self):
        return core.CharacterModifier(armor_ignore = 20)

    def get_passive_skill_list(self):

        
        #데몬스퓨리 : 보공15%, 링크에 반영되므로 미고려.
        DeathCurse = core.InformedCharacterModifier("데스 커스",pdamage = 1)
        Outrage = core.InformedCharacterModifier("아웃레이지",att = 50, crit = 20)
        PhisicalTraining = core.InformedCharacterModifier("피지컬 트레이닝",stat_main = 30, stat_sub = 30)
        Concentration = core.InformedCharacterModifier("컨센트레이션",pdamage_indep = 25)
        AdvancedWeaponMastery = core.InformedCharacterModifier("어드밴스드 웨폰 마스터리",att = 50, crit_damage = 15)
        
        DarkBindPassive = core.InformedCharacterModifier("다크 바인드(패시브)", armor_ignore = 30)
        
        return [DeathCurse, Outrage, PhisicalTraining, Concentration, AdvancedWeaponMastery, DarkBindPassive]

    def get_not_implied_skill_list(self):
        WeaponConstant = core.InformedCharacterModifier("무기상수", pdamage_indep = 20)
        Mastery = core.InformedCharacterModifier("숙련도",pdamage_indep = -5)        

        EvilTorture = core.InformedCharacterModifier("이블 토쳐",pdamage_indep = 15, crit = 15) #상태이상에 걸렷을때만.
        
        return [WeaponConstant, Mastery, EvilTorture]
        
    def generate(self, vEhc, chtr : ck.AbstractCharacter, combat : bool = False):
        '''
        코강 순서:
        슬래시-임팩트-서버-익스플로전-메타-데빌크라이

        #####하이퍼 #####
        # 데몬슬래시 - 리인포스, 리메인타임 리인포스
        # 데몬 입팩트 - 리인포스, 보너스 어택, 리듀스 포스        
        '''

    

        #Buff skills
        Booster = core.BuffSkill("부스터", 600, 180*1000, rem = True).wrap(core.BuffSkillWrapper)
        
        DemonSlash1 = core.DamageSkill("데몬 슬래시(1타)", 390, 110, 2, modifier = core.CharacterModifier(pdamage = 370)).setV(vEhc, 0, 2, False).wrap(core.DamageSkillWrapper)
        DemonSlash2 = core.DamageSkill("데몬 슬래시(2타)", 330, 110, 2, modifier = core.CharacterModifier(pdamage = 370)).setV(vEhc, 0, 2, False).wrap(core.DamageSkillWrapper)
        DemonSlash3 = core.DamageSkill("데몬 슬래시(3타)", 330, 100, 3, modifier = core.CharacterModifier(pdamage = 370)).setV(vEhc, 0, 2, False).wrap(core.DamageSkillWrapper)
        DemonSlash4 = core.DamageSkill("데몬 슬래시(4타)", 330, 100, 4, modifier = core.CharacterModifier(pdamage = 370)).setV(vEhc, 0, 2, False).wrap(core.DamageSkillWrapper)
        
        DemonSlashAW1 = core.DamageSkill("데몬 슬래시 강화(1타)", 390, 600, 3, modifier = core.CharacterModifier(pdamage = 370+50, armor_ignore = 50)).setV(vEhc, 0, 2, False).wrap(core.DamageSkillWrapper)
        DemonSlashAW2 = core.DamageSkill("데몬 슬래시 강화(2타)", 300, 600, 3, modifier = core.CharacterModifier(pdamage = 370+50, armor_ignore = 50)).setV(vEhc, 0, 2, False).wrap(core.DamageSkillWrapper)
        DemonSlashAW3 = core.DamageSkill("데몬 슬래시 강화(3타)", 210, 700, 3, modifier = core.CharacterModifier(pdamage = 370+50, armor_ignore = 50)).setV(vEhc, 0, 2, False).wrap(core.DamageSkillWrapper)
        DemonSlashAW4 = core.DamageSkill("데몬 슬래시 강화(4타)", 210, 800, 3, modifier = core.CharacterModifier(pdamage = 370+50, armor_ignore = 50)).setV(vEhc, 0, 2, False).wrap(core.DamageSkillWrapper)
    
        DemonSlashAWBB1 = core.DamageSkill("데몬 슬래시 강화(1타)블블", 390, 600, 3*1.9, modifier = core.CharacterModifier(pdamage = 370+50, armor_ignore = 50)).setV(vEhc, 0, 2, False).wrap(core.DamageSkillWrapper)
        DemonSlashAWBB2 = core.DamageSkill("데몬 슬래시 강화(2타)블블", 300, 600, 3*1.9, modifier = core.CharacterModifier(pdamage = 370+50, armor_ignore = 50)).setV(vEhc, 0, 2, False).wrap(core.DamageSkillWrapper)
        DemonSlashAWBB3 = core.DamageSkill("데몬 슬래시 강화(3타)블블", 210, 700, 3*1.9, modifier = core.CharacterModifier(pdamage = 370+50, armor_ignore = 50)).setV(vEhc, 0, 2, False).wrap(core.DamageSkillWrapper)
        DemonSlashAWBB4 = core.DamageSkill("데몬 슬래시 강화(4타)블블", 210, 800, 3*1.9, modifier = core.CharacterModifier(pdamage = 370+50, armor_ignore = 50)).setV(vEhc, 0, 2, False).wrap(core.DamageSkillWrapper)

        DemonSlashAWBB1_AuraWeapon = core.DamageSkill("오라 웨폰(1타)", 0, 600 * (75 + vEhc.getV(2,2))*0.01, 3*1.9, modifier = core.CharacterModifier(pdamage = 370+50, armor_ignore = 50)).wrap(core.DamageSkillWrapper)
        DemonSlashAWBB2_AuraWeapon = core.DamageSkill("오라 웨폰(2타)", 0, 600 * (75 + vEhc.getV(2,2))*0.01, 3*1.9, modifier = core.CharacterModifier(pdamage = 370+50, armor_ignore = 50)).wrap(core.DamageSkillWrapper)
        DemonSlashAWBB3_AuraWeapon = core.DamageSkill("오라 웨폰(3타)", 0, 700 * (75 + vEhc.getV(2,2))*0.01, 3*1.9, modifier = core.CharacterModifier(pdamage = 370+50, armor_ignore = 50)).wrap(core.DamageSkillWrapper)
        DemonSlashAWBB4_AuraWeapon = core.DamageSkill("오라 웨폰(4타)", 0, 800 * (75 + vEhc.getV(2,2))*0.01, 3*1.9, modifier = core.CharacterModifier(pdamage = 370+50, armor_ignore = 50)).wrap(core.DamageSkillWrapper)
        
        DemonImpact = core.DamageSkill("데몬 임팩트", 660, 460, (6+1)*1.9, modifier = core.CharacterModifier(crit = 100, armor_ignore = 30, boss_pdamage = 40, pdamage = 20)).setV(vEhc, 1, 2, False).wrap(core.DamageSkillWrapper)
        DemonImpact_AuraWeapon = core.DamageSkill("오라웨폰(데몬 임팩트)", 0, 460 * (75 + vEhc.getV(2,2))*0.01, (6+1)*1.9, modifier = core.CharacterModifier(crit = 100, armor_ignore = 30, boss_pdamage = 40, pdamage = 20)).wrap(core.DamageSkillWrapper)        

        DevilCry = core.DamageSkill("데빌 크라이", 1620, 515, 7*1.9, cooltime = 20 * 1000).setV(vEhc, 5, 2, False).wrap(core.DamageSkillWrapper)   #이블 토쳐 위해 사용필수.
        DevilCryBuff = core.BuffSkill("데빌 크라이(위협)", 0, 20000, cooltime = -1).wrap(core.BuffSkillWrapper)
        
        InfinityForce = core.BuffSkill("인피니티 포스", 990, 50*1000, cooltime = 200 * 1000).wrap(core.BuffSkillWrapper)
        Metamorphosis = core.BuffSkill("메타모포시스", 1680, 180*1000, rem = True, pdamage = 35).wrap(core.BuffSkillWrapper)
        MetamorphosisSummon = core.SummonSkill("메타모포시스(소환)", 0, 500, 250, 1, 180*1000, cooltime = -1).setV(vEhc, 4, 2, False).wrap(core.SummonSkillWrapper)
        
        #블루블러드는 소환수 적용이 안됨.
        BlueBlood = core.BuffSkill("블루 블러드", 1020, 60000, cooltime = 120000 - 60000).wrap(core.BuffSkillWrapper) #모든 공격에 최종데미지의 90%로 추가타 발생. 포스50수급시 -3초, 인피니티 포스시 4초마다 2초 감소, 모든 스킬 포스소모량 20%감소.
        Cerberus = core.DamageSkill("서버러스", 900, 450, 6, cooltime = 5000, modifier = core.CharacterModifier(boss_pdamage = 50, armor_ignore = 50)).setV(vEhc, 2, 2, False).wrap(core.DamageSkillWrapper)#포스50 추가흡수
        DemonFortitude = core.BuffSkill("데몬 포티튜드", 0, 60000, cooltime = 120000).wrap(core.BuffSkillWrapper)
        
        #5차스킬
        AuraWeaponBuff = core.BuffSkill("오라웨폰 버프", 0, (80 +2*vEhc.getV(2,2)) * 1000, cooltime = 180 * 1000, armor_ignore = 15, pdamage_indep = (vEhc.getV(1,1) // 5)).isV(vEhc,2,2).wrap(core.BuffSkillWrapper)  #두 스킬 syncronize 할 것!
        AuraWeaponCooltimeDummy = core.BuffSkill("오라웨폰(딜레이 더미)", 0, 4000, cooltime = -1).wrap(core.BuffSkillWrapper)   # 한 번 발동된 이후에는 4초간 발동되지 않도록 합니다.
    
        CallMastema = core.SummonSkill("콜 마스테마", 690, 5000, 1100, 8, (30+vEhc.getV(4,4))*1000, cooltime = 150*1000).isV(vEhc,4,4).wrap(core.SummonSkillWrapper)
        #CallMastemaAnother = core.SummonSkill("콜 마스테마+", 0, ).wrap(core.BuffSkillWrapper)    #러블리 테리토리..데미지 없음.
        
        DemonAwakning = core.BuffSkill("데몬 어웨이크닝", 1110, (35 + vEhc.getV(0,0))*1000, cooltime = 120 * 1000, crit = (50 + int(0.5*vEhc.getV(0,0)))).isV(vEhc,0,0).wrap(core.BuffSkillWrapper)
        DemonAwakningSummon = core.SummonSkill("데몬 어웨이크닝(더미)", 0, 8000, 0, 0, (35 + vEhc.getV(0,0))*1000, cooltime = -1).isV(vEhc,0,0).wrap(core.SummonSkillWrapper)
        
        SpiritOfRage = core.SummonSkill("요르문간드", 810, 1080, (850+34*vEhc.getV(3,3)), 9, (10+int(0.2*vEhc.getV(3,3)))*1000, cooltime = (120 - int(0.5*vEhc.getV(3,3)))*1000, modifier = core.CharacterModifier(crit = 100, armor_ignore = 50)).isV(vEhc,3,3).wrap(core.SummonSkillWrapper)
        SpiritOfRageEnd = core.DamageSkill("요르문간드(종료)", 0, 900+36*vEhc.getV(3,3), 12, cooltime = -1).isV(vEhc,3,3).wrap(core.DamageSkillWrapper)
        Orthros = core.SummonSkill("오르트로스(네메아)", 1000, 2000, 400+16*vEhc.getV(1,1), 12, 40000, cooltime = 120*1000, modifier = core.CharacterModifier(crit = 100, armor_ignore = 50)).isV(vEhc,1,1).wrap(core.SummonSkillWrapper)
        Orthros_ = core.SummonSkill("오르트로스(게리온)", 0, 3000, 900+36*vEhc.getV(1,1), 10, 40000, cooltime = -1, modifier = core.CharacterModifier(crit = 100, armor_ignore = 50)).isV(vEhc,1,1).wrap(core.SummonSkillWrapper)
        ######   Skill Wrapper   ######
        '''딜 사이클 정리
        어웨이크닝일 경우 -> 데몬슬래시
        어웨이크닝 없을 경우 -> 데몬 임팩트
        나머지 쿨마다 시전
        데빌 크라인 20초마다 시전
        서버러스 자동시전만 시전
        나머지는 알아서 시전
        
        가정 : 블블 100%
        
        TODO--> 포스 사용을 반영해서 블블 지속시간 시뮬레이션(엄청 어려울듯)
        '''
        DemonSlashAWBB1.onAfter(DemonSlashAWBB2)
        DemonSlashAWBB2.onAfter(DemonSlashAWBB3)
        DemonSlashAWBB3.onAfter(DemonSlashAWBB4)
        
        BasicAttack = core.OptionalElement(DemonAwakning.is_active, DemonSlashAWBB1, DemonImpact, name = "어웨이크닝 ON")
        BasicAttackWrapper = core.DamageSkill('기본 공격', 0,0,0).wrap(core.DamageSkillWrapper)
        BasicAttackWrapper.onAfter(BasicAttack)
        DevilCry.onAfter(DevilCryBuff)
        
        DemonAwakning.onAfter(DemonAwakningSummon)
        DemonAwakningSummon.onTick(Cerberus)
        
        SpiritOfRage.onAfter(SpiritOfRageEnd.controller((10+int(0.2*vEhc.getV(3,3)))*1000))
        Orthros.onAfter(Orthros_)
        
        Metamorphosis.onAfter(MetamorphosisSummon)

        # 오라 웨폰
        def AuraWeapon_connection_builder(origin_skill, target_skill):
            optional = core.OptionalElement(lambda : (AuraWeaponCooltimeDummy.is_not_active() and AuraWeaponBuff.is_active()), target_skill)
            origin_skill.onAfter(optional)
            target_skill.onAfter(AuraWeaponCooltimeDummy)
            
        AuraWeapon_connection_builder(DemonSlashAWBB1, DemonSlashAWBB1_AuraWeapon)
        AuraWeapon_connection_builder(DemonSlashAWBB2, DemonSlashAWBB2_AuraWeapon)
        AuraWeapon_connection_builder(DemonSlashAWBB3, DemonSlashAWBB3_AuraWeapon)
        AuraWeapon_connection_builder(DemonSlashAWBB4, DemonSlashAWBB4_AuraWeapon)
        AuraWeapon_connection_builder(DemonImpact, DemonImpact_AuraWeapon)
        
        return(BasicAttackWrapper,
                [globalSkill.maple_heros(chtr.level), globalSkill.useful_sharp_eyes(),
                    Booster, DevilCryBuff, InfinityForce, Metamorphosis, BlueBlood, DemonFortitude, AuraWeaponBuff, DemonAwakning,
                    globalSkill.soul_contract()] +\
                [Cerberus, DevilCry, SpiritOfRageEnd] +\
                [MetamorphosisSummon, CallMastema, DemonAwakningSummon, SpiritOfRage, Orthros, Orthros_] +\
                [AuraWeaponCooltimeDummy] +\
                [BasicAttackWrapper])