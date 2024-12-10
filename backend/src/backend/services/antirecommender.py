from typing import List, Optional, Tuple
import pandas as pd
import numpy as np
from numpy.typing import NDArray


class AntiRecommenderService:
    _instance: Optional["AntiRecommenderService"] = None
    _data: Optional[pd.DataFrame] = None
    data_path: Optional[str] = None

    def __new__(cls, data_path: str) -> "AntiRecommenderService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.data_path = data_path
        return cls._instance

    @property
    def data(self) -> pd.DataFrame:
        if self._data is None:
            if not self.data_path:
                raise ValueError("Data path must be set before accessing the data.")
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
    ) -> Tuple[NDArray[np.float64], NDArray[np.object_]]:
        user_tracks = self._get_user_tracks(user_track_ids)
        numerical_profile: NDArray[np.float64] = (
            user_tracks[self.numerical_features].mean(axis=0).values
        )
        categorical_profile: NDArray[np.object_] = (
            user_tracks[self.categorical_features].mode(axis=0).iloc[0].values
        )
        return numerical_profile, categorical_profile

    def _calculate_dissimilarities(
        self,
        numerical_profile: NDArray[np.float64],
        categorical_profile: NDArray[np.object_],
    ) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
        numerical_data: NDArray[np.float64] = self.data[self.numerical_features].values
        categorical_data: NDArray[np.object_] = self.data[
            self.categorical_features
        ].values
        numerical_dissimilarity: NDArray[np.float64] = np.linalg.norm(
            numerical_data - numerical_profile, axis=1
        )
        categorical_dissimilarity: NDArray[np.float64] = np.sum(
            categorical_data != categorical_profile, axis=1
        ) / len(self.categorical_features)
        return numerical_dissimilarity, categorical_dissimilarity

    def _combine_dissimilarities(
        self,
        numerical_dissimilarity: NDArray[np.float64],
        categorical_dissimilarity: NDArray[np.float64],
        alpha: float,
    ) -> NDArray[np.float64]:
        return alpha * numerical_dissimilarity + (1 - alpha) * categorical_dissimilarity

    def _get_candidate_tracks(
        self, user_track_ids: List[str], combined_dissimilarity: NDArray[np.float64]
    ) -> pd.DataFrame:
        self.data["combined_dissimilarity"] = combined_dissimilarity
        return self.data[~self.data["track_id"].isin(user_track_ids)]

    def _select_track_id(self, candidates: pd.DataFrame, index: int) -> str:
        return str(
            candidates.sort_values("combined_dissimilarity", ascending=False).iloc[
                index
            ]["track_id"]
        )

    def antirecommend(
        self, user_track_ids: List[str], alpha: float = 0.7, index: int = 245
    ) -> str:
        """
        Finds and returns a track ID that is most dissimilar to the provided user track IDs.

        This function calculates the dissimilarity of all tracks in the dataset to a
        user-defined set of tracks, based on both numerical and categorical features.
        It then returns the track ID of the track at the specified position in the sorted
        list of most dissimilar tracks.

        Args:
            user_track_ids (List[str]): A list of track IDs representing the user's preferences.
            alpha (float): A weighting factor for numerical versus categorical dissimilarities.
                        Defaults to 0.7, giving 70% weight to numerical features.
            index (int): The position in the sorted list of dissimilar tracks to return.
                        Defaults to 245.

        Returns:
            str: The track ID of the track at the specified index in the sorted dissimilarity list.
        """
        numerical_profile, categorical_profile = self._calculate_profiles(
            user_track_ids
        )
        numerical_dissimilarity, categorical_dissimilarity = (
            self._calculate_dissimilarities(numerical_profile, categorical_profile)
        )
        combined_dissimilarity = self._combine_dissimilarities(
            numerical_dissimilarity, categorical_dissimilarity, alpha
        )
        candidates = self._get_candidate_tracks(user_track_ids, combined_dissimilarity)
        return self._select_track_id(candidates, index)
