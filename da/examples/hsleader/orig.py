# -*- generated by 1.0.9 -*-
import da
PatternExpr_245 = da.pat.TuplePattern([da.pat.ConstantPattern('Leader'), da.pat.FreePattern('leader')])
PatternExpr_275 = da.pat.TuplePattern([da.pat.ConstantPattern('Token'), da.pat.FreePattern('v'), da.pat.FreePattern('direction'), da.pat.FreePattern('h')])
PatternExpr_286 = da.pat.FreePattern('source')
PatternExpr_443 = da.pat.TuplePattern([da.pat.ConstantPattern('Leader'), da.pat.FreePattern('leader')])
PatternExpr_450 = da.pat.FreePattern('source')
_config_object = {}
import sys
import random

class P(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._PReceivedEvent_0 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_0', PatternExpr_245, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_1', PatternExpr_275, sources=[PatternExpr_286], destinations=None, timestamps=None, record_history=None, handlers=[self._P_handler_274]), da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_2', PatternExpr_443, sources=[PatternExpr_450], destinations=None, timestamps=None, record_history=None, handlers=[self._P_handler_442])])

    def setup(self, left, right, **rest_551):
        super().setup(left=left, right=right, **rest_551)
        self._state.left = left
        self._state.right = right
        self._state.status = 'Unknown'
        (self._state.phase_left, self._state.phase_right) = (False, False)
        self._state.phase = 0

    def run(self):
        while True:
            self.send(('Token', self._id, 'out', (1 << self._state.phase)), to={self._state.left, self._state.right})
            super()._label('_st_label_211', block=False)
            leader = None

            def ExistentialOpExpr_243():
                nonlocal leader
                for (_, _, (_ConstantPattern260_, leader)) in self._PReceivedEvent_0:
                    if (_ConstantPattern260_ == 'Leader'):
                        if True:
                            return True
                return False
            _st_label_211 = 0
            while (_st_label_211 == 0):
                _st_label_211 += 1
                if (self._state.status == 'Leader'):
                    self.output(('I am leader at phase %d!' % self._state.phase))
                    self.send(('Leader', self._id), to={self._state.left, self._state.right})
                    break
                    _st_label_211 += 1
                elif (self._state.phase_left and self._state.phase_right):
                    self._state.phase += 1
                    (self._state.phase_left, self._state.phase_right) = (False, False)
                    _st_label_211 += 1
                elif ExistentialOpExpr_243():
                    self.output(('Leader is ' + str(leader)))
                    break
                    _st_label_211 += 1
                else:
                    super()._label('_st_label_211', block=True)
                    _st_label_211 -= 1
            else:
                if (_st_label_211 != 2):
                    continue
            if (_st_label_211 != 2):
                break

    def _P_handler_274(self, v, direction, h, source):
        if ((source == self._state.left) and (direction == 'out')):
            if ((v > self._id) and (h > 1)):
                self.send(('Token', v, 'out', (h - 1)), to=self._state.right)
            elif ((v > self._id) and (h == 1)):
                self.send(('Token', v, 'in', 1), to=self._state.left)
            elif (v == self._id):
                self._state.status = 'Leader'
        elif ((source == self._state.right) and (direction == 'out')):
            if ((v > self._id) and (h > 1)):
                self.send(('Token', v, 'out', (h - 1)), to=self._state.left)
            elif ((v > self._id) and (h == 1)):
                self.send(('Token', v, 'in', 1), to=self._state.right)
            elif (v == self._id):
                self._state.status = 'Leader'
        elif ((source == self._state.left) and (direction == 'in')):
            if (v > self._id):
                self.send(('Token', v, 'in', 1), to=self._state.right)
            elif (v == self._id):
                self._state.phase_left = True
        elif ((source == self._state.right) and (direction == 'in')):
            if (v > self._id):
                self.send(('Token', v, 'in', 1), to=self._state.left)
            elif (v == self._id):
                self._state.phase_right = True
    _P_handler_274._labels = None
    _P_handler_274._notlabels = None

    def _P_handler_442(self, leader, source):
        if (source == self._state.left):
            self.send(('Leader', leader), to=self._state.right)
        else:
            self.send(('Leader', leader), to=self._state.left)
    _P_handler_442._labels = None
    _P_handler_442._notlabels = None

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([])
    _config_object = {'channel': 'fifo'}

    def run(self):
        n = (int(sys.argv[1]) if (len(sys.argv) > 1) else 10)
        topology = list(self.new(P, num=n))
        random.shuffle(topology)
        for (i, p) in enumerate(topology):
            if (i == (len(topology) - 1)):
                self._setup({p}, (topology[(i - 1)], topology[0]))
            else:
                self._setup({p}, (topology[(i - 1)], topology[(i + 1)]))
        self._start(topology)
