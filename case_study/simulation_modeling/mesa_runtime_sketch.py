# --- 1. Resident agent ---
class ResidentAgent(mesa.Agent):
    def __init__(self, unique_id, model, trust, risk):
        super().__init__(unique_id, model)
        self.trust_in_official = trust   # in [0, 1]
        self.risk_preference = risk      # illustrative prompt-facing descriptor
        self.belief_state = "unaware"
        self.memory = MessageBuffer(capacity=10)

    def step(self):
        msgs = self.perceive_messages()          # official, media, rumor, peers
        history = self.memory.retrieve()
        # Reasoning: LLM integrates conflicting messages given trust and risk
        decision = llm_engine.generate(
            role="Resident", profile=(self.trust_in_official, self.risk_preference),
            messages=msgs, memory=history)
        self.belief_state = decision["perceived_threat_level"]
        if decision["action"] == "EVACUATE":
            self.evacuate()
        elif decision["action"] == "FORWARD":
            self.forward_to_neighbors(decision["message"])
        # else: keep waiting

# --- 2. SocialPlatform agent in a RumorSource role ---
class SocialPlatformAgent(mesa.Agent):
    def step(self):
        official = self.model.latest_official_message()
        # Reasoning: LLM distorts the official message to maximise spread
        rumor = llm_engine.generate(
            role="RumorSource", distortion="high", react_to=official)
        self.model.inject(rumor, audience=rumor["intended_audience"])

# --- 3. Environment (world engine) ---
class AlertModel(mesa.Model):
    def step(self):
        if self.time_step >= self.official_delay:    # delta: official response delay
            self.broadcast(self.official_message(), reach="all")
        self.schedule.step()                          # residents and rumor source act
        self.update_reachability()                    # route messages along the network
