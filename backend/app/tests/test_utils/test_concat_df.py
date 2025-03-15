import pandas as pd
import pytest

from scraper.scraper_func.utils import concat_df_list


def test_concatenate_multiple_non_empty_dataframes():
    # Given
    df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    df2 = pd.DataFrame({"A": [5, 6], "B": [7, 8]})
    df_list = [df1, df2]

    # When
    result = concat_df_list(df_list)

    # Then
    assert not result.empty
    assert result.equals(pd.concat([df1, df2]))


def test_concatenate_empty_list():
    # Given
    df_list = []

    # When
    result = concat_df_list(df_list)

    # Then
    assert len(result) == 0


def test_concatenate_dataframes_with_missing_values():
    # Given
    df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    df2 = pd.DataFrame({"A": [5, 6], "B": [7, None]})
    df_list = [df1, df2]

    # When
    result = concat_df_list(df_list)

    # Then
    assert not result.empty
    assert result.equals(pd.concat([df1, df2]))


def test_concatenate_mixed_empty_non_empty_dataframes():
    # Given
    df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    df2 = pd.DataFrame({"A": [5, 6], "B": [7, 8]})
    df3 = pd.DataFrame()  # Empty DataFrame
    df_list = [df1, df2, df3]

    # When
    result = concat_df_list(df_list)

    # Then
    assert not result.empty
    assert result.equals(pd.concat([df1, df2]))


def test_concatenate_dataframes_with_different_index_types():
    # Given
    df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    df2 = pd.DataFrame({"A": [5, 6], "B": [7, 8]})
    df1.index = ["a", "b"]
    df2.index = ["c", "d"]
    df_list = [df1, df2]

    # When
    result = concat_df_list(df_list)

    # Then
    assert not result.empty
    assert result.equals(pd.concat([df1, df2]))


def test_concatenate_dataframes_with_duplicate_indices():
    # Given
    df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]}, index=[0, 1])
    df2 = pd.DataFrame({"A": [5, 6], "B": [7, 8]}, index=[1, 2])
    df_list = [df1, df2]

    # When
    result = concat_df_list(df_list)

    # Then
    assert not result.empty
    assert result.equals(pd.concat([df1, df2]))


if __name__ == "__main__":
    pytest.main()
