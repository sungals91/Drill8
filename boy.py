#from importlib.metadata import pass_none
from pico2d import load_image, get_time
from state_machine import *


#상태를 클래스를 통해서 정의함
class Idle:
    @staticmethod # @는 데코레이터 기능. 함수의 기능을 조금 바꾼다.
    # 뒤에 이어서 모는 함수는 staticmethod함수로 간주. 멤버 변수가 아니라 클래스 안 객체와 상관없는 함수
    # 객체를 찍어내는 목적이 아니라 클래스라는 그룹으로 함수를 묶어놓는 목적
    def enter(boy, e):
        boy.start_time = get_time() # 현재 시간을 저장
        boy.frame = 0
        boy.dir = 0 # 정지상태
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1
    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy): # 파라미터로 boy를 쓰나 a를 쓰나 같음
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.add_event(('TIME_OUT', 0))
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Sleep:
    @staticmethod
    def enter(boy, e):
        if start_event(e):
            boy.face_dir = 1
            boy.action = 3
        boy.frame = 0
        pass
    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_composite_draw(
                boy.frame * 100, 300, 100, 100, 3.141592/2, '', boy.x - 25, boy.y - 25, 100, 100
            )
        elif boy.face_dir == -1:
            boy.image.clip_composite_draw(
                boy.frame * 100, 200, 100, 100, -3.141592 / 2, '', boy.x + 25, boy.y - 25, 100, 100
            )

class Run:
    @staticmethod
    def enter(boy, e):
        #boy.dir = 1 # 오른쪽 방향
        #boy.action = 1
        #boy.frame = 0
        if right_down(e) or left_up(e):
            boy.dir, boy.action = 1, 1
        elif left_down(e) or right_up(e):
            boy.dir, boy.action = -1, 0
        pass
    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.x += boy.dir * 5
        boy.frame = (boy.frame + 1) % 8
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y
        )
        pass



class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 소년 객체의 스테이트머신 생성
        # 상태를 나타낼 떄 필요한 4가지 Do activity, Exit action, Entry action + draw
        self.state_machine.start(Idle) # 초기상태 결정
        self.state_machine.set_transitions(
            {
                Run : {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle}, # Run 상태에서 어떤 이벤트가 들어와도 처리하지 않겠다
                Idle : {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep},
                Sleep : {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down : Idle}
            }
        )


    def update(self):
        self.state_machine.update() # 상태머신으로 조절
        #self.frame = (self.frame + 1) % 8

    def handle_event(self, event):
        # event : 입력 이벤트 key mouse
        # 우리가 state machine 전달해줄건 ( , )
        self.state_machine.add_event(
            ('INPUT', event)
        )

    def draw(self):
        self.state_machine.draw()
        #self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, self.x, self.y)
