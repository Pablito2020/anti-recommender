from typing import List, Tuple, Any, Optional
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

DEFAULT_NUMBER_CLUSTERS = 30


class AntiRecommenderService:
    _instance: Optional["AntiRecommenderService"] = None
    _data: pd.DataFrame = None
    _clusters_centers: Optional[np.ndarray[Any, np.dtype[np.float64]]] = None
    data_path: str = ""
    num_clusters: int = DEFAULT_NUMBER_CLUSTERS

    def __new__(
        cls, data_path: str, num_clusters: int = DEFAULT_NUMBER_CLUSTERS
    ) -> "AntiRecommenderService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.data_path = data_path
            cls._instance.num_clusters = num_clusters
        return cls._instance

    @property
    def data(self) -> pd.DataFrame:
        if self._data is None:
            self._data = pd.read_csv(self.data_path)
        return self._data

    @property
    def numerical_features(self) -> List[str]:
        return [
            "popularity",
            "longness",
            "danceability",
            "energy",
            "loudness",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
        ]

    @property
    def categorical_features(self) -> List[str]:
        return ["time_signature", "mode", "explicit", "key", "track_genre"]

    def _get_user_tracks(self, user_track_ids: List[str]) -> pd.DataFrame:
        return self.data[self.data["track_id"].isin(user_track_ids)]

    def _calculate_profiles(
        self, user_track_ids: List[str]
    ) -> Tuple[
        np.ndarray[Any, np.dtype[np.float64]], np.ndarray[Any, np.dtype[np.object_]]
    ]:
        user_tracks = self._get_user_tracks(user_track_ids)
        numerical_profile = user_tracks[self.numerical_features].mean(axis=0).values
        categorical_profile = (
            user_tracks[self.categorical_features].mode(axis=0).iloc[0].values
        )
        return numerical_profile, categorical_profile

    def _initialize_clusters(self) -> None:
        numerical_data = self.data[self.numerical_features].values
        kmeans = KMeans(n_clusters=self.num_clusters, random_state=42)
        self.data["cluster"] = kmeans.fit_predict(numerical_data)
        self._clusters_centers = kmeans.cluster_centers_

    def _get_cluster_of_tracks(self, track_ids: List[str]) -> int:
        user_tracks = self._get_user_tracks(track_ids)
        user_cluster = user_tracks["cluster"].mode().iloc[0]
        return int(user_cluster)

    def _find_furthest_cluster(self, user_cluster: int) -> int:
        assert (
            self._clusters_centers is not None
        ), "You shouldn't call this if we don't have any clusters..."
        distances = cdist(
            [self._clusters_centers[user_cluster]],
            self._clusters_centers,
            metric="euclidean",
        )
        furthest_cluster = np.argmax(distances)
        return int(furthest_cluster)

    def _get_most_similar_song_in_cluster(
        self,
        cluster: int,
        numerical_profile: np.ndarray[Any, np.dtype[np.float64]],
        categorical_profile: np.ndarray[Any, np.dtype[np.object_]],
        alpha: float,
    ) -> str:
        """
        Do:
            - For each numerical value of the dataset:
               | Song id | num. value 1 | num. value 2 | ...  |
               |   x1    |     x1a      |    x1b       | ...  |
               |   x2    |     x2a      |    x2b       | ...  |
            - And our numerical values:
               |   ___   |    alpha1    |    alpha2    | ...  |
            Do:
               |   x1    | x1a - alpha1 | x1b - alpha2 | ...  |
               |   x2    | x2a - alpha1 | x2b - alpha2 | ...  |

            - For each categorical value of the dataset:
               | Song id | cat. value 1 | cat. value 2 | ...  |
               |   x1    |     x1a      |    x1b       | ...  |
               |   x2    |     x2a      |    x2b       | ...  |
            - And our categorical values:
               |   ___   |    alpha1    |    alpha2    | ...  |
            Do:
             (in python, just like C, 1 it's True and 0 is False)
               |   x1    | x1a != alpha1 | x1b != alpha2 | ...  |
               |   x2    | x2a != alpha1 | x2b != alpha2 | ...  |
               This means, if categorical are different, the rows will have more 1's
               If they are similar, they will have more 0's

            Then, we combine both distances and get the minimum one for the closest song

        """
        cluster_songs = self.data[self.data["cluster"] == cluster]
        numerical_distances = np.linalg.norm(
            cluster_songs[self.numerical_features].values - numerical_profile, axis=1
        )
        categorical_distances = np.sum(
            cluster_songs[self.categorical_features].values != categorical_profile,
            axis=1,
        ) / len(self.categorical_features)
        combined_distances = (
            alpha * numerical_distances + (1 - alpha) * categorical_distances
        )
        closest_song_index = np.argmin(combined_distances)
        return str(cluster_songs.iloc[closest_song_index]["track_id"])

    def antirecommend(self, user_track_ids: List[str], alpha: float = 0.6) -> str:
        """
        Finds and returns a track ID that is outside the user's comfort zone but still somewhat similar.

        This function identifies the user's cluster, finds the furthest away cluster, and selects
        the most similar song in that cluster to the user's profile.

        Args:
            user_track_ids (List[str]): A list of track IDs representing the user's preferences.
            alpha (float): A weighting factor for numerical versus categorical dissimilarities.

        Returns:
            str: The track ID of the recommended song.
        """
        if self._clusters_centers is None:
            self._initialize_clusters()

        numerical_profile, categorical_profile = self._calculate_profiles(
            user_track_ids
        )
        user_cluster = self._get_cluster_of_tracks(user_track_ids)
        furthest_cluster = self._find_furthest_cluster(user_cluster)
        return self._get_most_similar_song_in_cluster(
            furthest_cluster, numerical_profile, categorical_profile, alpha
        )

    def filter_existing_tracks(self, track_ids: List[str]) -> List[str]:
        """
        Filters out any track IDs that are not present in the dataset.

        Args:
            track_ids (List[str]): A list of track IDs to filter.

        Returns:
            List[str]: A list of track IDs that are present in the dataset.

        """
        return [
            track_id
            for track_id in track_ids
            if track_id in self.data["track_id"].values
        ]

    def get_random_track(self) -> str:
        """
        Returns a random track ID.

        Returns:
            str: A random track ID present in the dataset.

        """
        return str(self.data.sample(n=1)["track_id"].iloc[0])


_anti_recommender = AntiRecommenderService(
    data_path="./data/spotify_tracks_dataset.csv"
)


async def get_anti_recommender() -> AntiRecommenderService:
    return _anti_recommender
