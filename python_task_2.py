import pandas as pd
from geopy.distance import geodesic

df = pd.read_csv('dataset-2.csv')


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here

    distance_matrix = pd.DataFrame(index=df['ID'], columns=df['ID'])

    for i in range(len(df)):
        for j in range(i, len(df)):
            distance = geodesic((df.loc[i, 'Latitude'], df.loc[i, 'Longitude']),
                                (df.loc[j, 'Latitude'], df.loc[j, 'Longitude'])).miles

            distance_matrix.at[df.loc[i, 'ID'], df.loc[j, 'ID']] = distance
            distance_matrix.at[df.loc[j, 'ID'], df.loc[i, 'ID']] = distance

        distance_matrix.values[[range(len(df))] * 2] = 0



    return distance_matrix


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here

    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            id_start = df.index[i]
            id_end = df.columns[j]
            distance = df.at[id_start, id_end]

            unrolled_df = unrolled_df.append({'id_start': id_start, 'id_end': id_end, 'distance': distance},
                                             ignore_index=True)

    return unrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """

    reference_df = df[df['id_start'] == reference_id]


    if reference_df.empty:
        raise ValueError(f"Reference ID {reference_id} not found in the DataFrame.")


    average_distance = reference_df['distance'].mean()


    threshold = 0.1 * average_distance


    within_threshold_df = df[
        (df['distance'] >= average_distance - threshold) & (df['distance'] <= average_distance + threshold)
        ]

    return within_threshold_df




    return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here

    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}


    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df




def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

    weekday_time_ranges = [(time(0, 0, 0), time(10, 0, 0)),
                           (time(10, 0, 0), time(18, 0, 0)),
                           (time(18, 0, 0), time(23, 59, 59))]

    weekend_time_ranges = [(time(0, 0, 0), time(23, 59, 59))]


    weekday_discount_factors = [0.8, 1.2, 0.8]
    weekend_discount_factor = 0.7


    df['start_day'] = ""
    df['start_time'] = ""
    df['end_day'] = ""
    df['end_time'] = ""


    for i, (start_time, end_time) in enumerate(weekday_time_ranges):
        mask = (df['start_time'] >= start_time) & (df['end_time'] <= end_time) & (
            df['start_day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']))
        df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= weekday_discount_factors[i]

    for (start_time, end_time) in weekend_time_ranges:
        mask = (df['start_time'] >= start_time) & (df['end_time'] <= end_time) & (
            df['start_day'].isin(['Saturday', 'Sunday']))
        df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= weekend_discount_factor

    return df

