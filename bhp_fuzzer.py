from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator
from java.util import List, ArrayList
import random

class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        callbacks.registerIntruderPayloadGeneratorFactory(self)
        return

    def getGeneratorName(self):
        return 'BHP Payload Generator'

    def createNewInstance(self, attack):
        return BHPFuzzer(self, attack)

class BHPFuzzer(IIntruderPayloadGenerator):
    def __init__(self, extender, attack):
        self.extender = extender
        self.helpers = extender._helpers
        self.attack = attack
        self.max_payloads = 10
        self.num_iterations = 0

        return

    def hasMorePayloads(self):
        if self.num_iterations == self.max_payloads:
            return False
        else:
            return True

    def getNextPayload(self, current_payload):
        # convert byte array to string
        payload = ''.join(chr(x) for x in current_payload)
        payload = self.mutate_payload(payload)
        self.num_iterations += 1

        return payload

    def reset(self):
        self.num_iterations = 0
        return

    def mutate_payload(self, original_payload):
        # pick a simple mutator or even call an external script
        picker = random.randint(1, 3)
        
        # select a random offset in the payload to mutate
        offset = random.randint(0, len(original_payload) - 1)
        front, back = original_payload[:offset], original_payload[offset:]

        # random offset insert a SQL injection attempt
        if picker == 1:
            front += "'"
        # jam an XSS attempt in
        elif picker == 2:
            front += "<script>alert('BHP!');</script>"
        # repeat a random chunk of the original payload
        elif picker == 3:
            chunk_length = random.randint(0, len(back)-1)
            repeater = random.randint(1, 10)
            for _ in range(repeater):
                front += original_payload[:offset + chunk_length]

        return front + back