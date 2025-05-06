from PyQt6.QtCore import Qt, pyqtSignal, QObject


class DraftController(QObject):
    draft_updated = pyqtSignal()
    wheel_spun = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.choices = ["Amy", "Big", "Gamma", "Knuckles", "Super Sonic", "Tails"]
        self.colors = ["#f6a6c1", "#5132fa", "#797979", "#ff1400", "#e2d000", "#ffa901"]

        self.draft_phase = 0
        self.draft_phases = ["Wheel Picking", "Player 1 Banning", "Player 2 Banning", "Player 2 Picking", "Player 1 Picking", "Draft Complete!"]

        self.bans = []
        self.picks = []
        self.p1_choices = []
        self.p2_choices = []
        self.history = []

    def available_choices(self):
        available = []
        for choice in self.choices:
            if choice in self.picks or choice in self.bans:
                continue
            available.append(choice)
        return available
    
    def next_phase(self):
        if self.draft_phase < len(self.draft_phases) - 1:
            self.draft_phase += 1
            self.draft_updated.emit()
    
    def make_choice(self, story):
        match self.draft_phase:
            case 0:
                self.picks.append(story)
                self.history.append(("wheel", "pick"))
            case 1:
                self.bans.append(story)
                self.p1_choices.append((story, "ban"))
                self.history.append(("p1", "ban"))
            case 2:
                self.bans.append(story)
                self.p2_choices.append((story, "ban"))
                self.history.append(("p2", "ban"))
            case 3:
                self.picks.append(story)
                self.p2_choices.append((story, "pick"))
                self.history.append(("p2", "pick"))
            case 4:
                self.picks.append(story)
                self.p1_choices.append((story, "pick"))
                self.history.append(("p1", "pick"))
        
        self.next_phase()

    def spin_wheel(self):
        self.wheel_spun.emit()
    
    def wheel_result(self, result):
        self.picks.append(result)
        self.history.append(("wheel", "pick"))
        self.next_phase()
    
    def reset_draft(self):
        self.draft_phase = 0
        self.bans.clear()
        self.picks.clear()
        self.p1_choices.clear()
        self.p2_choices.clear()
        self.history.clear()
        self.draft_updated.emit()
    
    def undo_last_action(self):
        if self.draft_phase <= 0:
            return

        self.draft_phase -= 1
        if self.history[-1][1] == "pick":
            self.picks.pop()
        if self.history[-1][1] == "ban":
            self.bans.pop()
        if self.history[-1][0] == "p1":
            self.p1_choices.pop()
        if self.history[-1][0] == "p2":
            self.p2_choices.pop()

        self.history.pop()
        self.draft_updated.emit()
