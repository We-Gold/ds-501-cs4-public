import geopandas as gpd
import numpy as np
from shapely.geometry import Point

DEFAULT_SAMPLE_SIZE = 100000


def generate_uniform_points_by_count(gdf, n_points=DEFAULT_SAMPLE_SIZE):
    """
    Generate ~n_points uniformly spaced over the geometry in gdf.

    Parameters:
    - gdf: GeoDataFrame of polygons
    - n_points: desired number of points (approximate, clipped to geometry)

    Returns:
    - GeoDataFrame of points within the geometry
    """
    bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
    minx, miny, maxx, maxy = bounds
    area = (maxx - minx) * (maxy - miny)

    # Estimate spacing based on area and target point count
    estimated_spacing = np.sqrt(area / n_points)

    # Create grid using estimated spacing
    x_coords = np.arange(minx, maxx, estimated_spacing)
    y_coords = np.arange(miny, maxy, estimated_spacing)
    mesh_x, mesh_y = np.meshgrid(x_coords, y_coords)

    # Flatten and convert to Points
    points = [Point(x, y) for x, y in zip(mesh_x.ravel(), mesh_y.ravel())]
    points_gdf = gpd.GeoDataFrame(geometry=points, crs=gdf.crs)

    # Clip to geometry
    clipped_points = points_gdf[points_gdf.within(gdf.unary_union)]

    return clipped_points


def compute_dist_to_nearest_point(gdf: gpd.GeoDataFrame, points_gdf: gpd.GeoDataFrame):
    """
    Compute the distance from each point in gdf to the nearest point in points_df.

    Parameters:
    - gdf: GeoDataFrame of points
    - points_gdf: GeoDataFrame of points to compute distances to

    Returns:
    - GeoDataFrame with distances in km added as a new column
    """

    # Ensure both GeoDataFrames have the same CRS
    if gdf.crs != points_gdf.crs:
        points_gdf = points_gdf.to_crs(gdf.crs)

    # Create a spatial index for the points_gdf GeoDataFrame
    spatial_index = points_gdf.sindex
    distances = []

    nearest_for_each = spatial_index.nearest(gdf.geometry, return_all=False)[1]

    for idx, geom in enumerate(gdf.geometry):
        # Find the nearest point using the spatial index
        nearest_idx = nearest_for_each[idx]
        nearest_geom = points_gdf.geometry.iloc[nearest_idx]

        # Calculate the distance to the nearest point
        distance = geom.distance(nearest_geom)

        distances.append(distance)

    gdf["Distance to Nearest Stop (km)"] = distances

    # Convert distances to meters if the CRS is in degrees
    if gdf.crs.is_geographic:
        gdf["Distance to Nearest Stop (km)"] = gdf[
            "Distance to Nearest Stop (km)"
        ].apply(
            lambda x: x * 111.139
        )  # Approximate conversion factor for degrees to meters

    return gdf
