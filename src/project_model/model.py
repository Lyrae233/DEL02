import mesa
import networkx as nx
from itertools import combinations

from agents import AutoplayAgent


class SpotifyAutoplayModel(mesa.Model):

    def __init__(self, artist_weight=0.5, rng=42):
        super().__init__(rng=rng)

        # Recommendation weights
        self.artist_weight = artist_weight
        self.genre_weight = 1 - artist_weight
        self.base_weight = 0.1

        # Create a synthetic music catalogue
        self.catalogue = {}
        self.network = nx.Graph()

        genres = ["Pop", "Rock", "Jazz", "Hip-Hop", "Electronic"]

        for artist_id in range(10):
            main_genre = genres[artist_id % 5]

            for track_id in range(5):
                song_id = f"song_{artist_id}_{track_id}"

                # Give each artist one cross-genre song
                genre = (
                    genres[(artist_id + 1) % 5]
                    if track_id == 4
                    else main_genre
                )

                song = {
                    "artist": f"artist_{artist_id}",
                    "genre": genre
                }

                self.catalogue[song_id] = song
                self.network.add_node(song_id, **song)

        # Create weighted connections between songs
        for song_a, song_b in combinations(self.catalogue, 2):
            weight = self.transition_score(song_a, song_b)
            self.network.add_edge(song_a, song_b, weight=weight)

        # Initial conditions
        self.current_song = "song_0_0"
        self.familiar_artists = {"artist_0", "artist_1"}
        self.transitions = []

        # Create the recommendation agent
        self.recommender = AutoplayAgent(self)

    def transition_score(self, current_song, candidate_song):
        current = self.catalogue[current_song]
        candidate = self.catalogue[candidate_song]

        same_artist = current["artist"] == candidate["artist"]
        same_genre = current["genre"] == candidate["genre"]

        score = self.base_weight
        score += self.artist_weight * int(same_artist)
        score += self.genre_weight * int(same_genre)

        return score

    def record_transition(self, current_song, next_song):
        current = self.catalogue[current_song]
        selected = self.catalogue[next_song]

        same_artist = current["artist"] == selected["artist"]
        same_genre = current["genre"] == selected["genre"]

        if same_artist and same_genre:
            category = "same_artist_same_genre"
        elif same_artist:
            category = "same_artist_different_genre"
        elif same_genre:
            category = "different_artist_same_genre"
        else:
            category = "neither_match"

        self.transitions.append({
            "step": len(self.transitions) + 1,
            "from_song": current_song,
            "to_song": next_song,
            "category": category,
            "unfamiliar_artist": (
                selected["artist"] not in self.familiar_artists
            )
        })

    def step(self):
        self.agents.do("step")
