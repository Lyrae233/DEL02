import mesa


class AutoplayAgent(mesa.Agent):
    
    def __init__(self, model):
        super().__init__(model)

    def step(self):
        # Get the currently playing song
        current_song = self.model.current_song

        # Find candidate songs, excluding the current song
        candidates = [
            song_id
            for song_id in self.model.catalogue
            if song_id != current_song
        ]

        # Calculate a selection score for each candidate
        scores = [
            self.model.transition_score(current_song, song_id)
            for song_id in candidates
        ]

        # Randomly select the next song using weighted probabilities
        next_song = self.random.choices(
            candidates,
            weights=scores,
            k=1
        )[0]

        # Record the transition
        self.model.record_transition(current_song, next_song)

        # Update the currently playing song
        self.model.current_song = next_song
