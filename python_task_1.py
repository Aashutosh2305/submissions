import pandas as pd

df = pd.read_csv('dataset-1.csv')


def generate_car_matrix(df) -> pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values,
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here

    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    for col in car_matrix.columns:
        car_matrix.loc[col, col] = 0

    return car_matrix


def get_type_count(df) -> dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    type_counts = df['car_type'].value_counts().to_dict()

    return type_counts


def get_bus_indexes(df) -> list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here

    mean_bus_value = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * mean_bus_value].index.tolist()

    return bus_indexes


def filter_routes(df) -> list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here

    route_avg_truck = df.groupby('route')['truck'].mean()

    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    return filtered_routes


def multiply_matrix(matrix) -> pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    condition1 = result_matrix > 20
    condition2 = result_matrix <= 20

    result_matrix[condition1] *= 0.75
    result_matrix[condition2] *= 1.25

    result_matrix = result_matrix.round(1)

    return result_matrix


def time_check(df) -> pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['day_of_week'] = df['timestamp'].dt.day_name()
    df['time'] = df['timestamp'].dt.time

    completeness_check = df.groupby(['id', 'id_2'])[['day_of_week', 'time']].agg({'day_of_week': lambda x: sorted(
        x.unique()) == ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                                                                                  'time': lambda x: (
                                                                                              min(x) == pd.timestamp(
                                                                                          '00:00:00') and max(
                                                                                          x) == pd.timestamp(
                                                                                          '23:59:59'))
                                                                                  })

    return completeness_check.all(axis=1)
