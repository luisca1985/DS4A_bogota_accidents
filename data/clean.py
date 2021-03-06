import pandas as pd
import geopandas as gpd

def get_data_cleaned():
    df = pd.read_csv ('data/historico_siniestros_bogota.csv', delimiter=',')
    df.isnull().any()

    # Relevance
    #Drop X and Y columns
    df = df.drop(["X", "Y"], axis=1)
    #Drop FECHA_OCURRENCIA_ACC and ANO_OCURRENCIA_ACC
    df = df.drop(["FECHA_OCURRENCIA_ACC","ANO_OCURRENCIA_ACC"], axis=1)
    #Replace each missing row in CIV and PK_CALZADA with the "Not Available" string
    df["CIV"] = df["CIV"].astype(str)
    df["CIV"] = df["CIV"].fillna("Not Available")
    df["PK_CALZADA"] = df["PK_CALZADA"].astype(str)
    df["PK_CALZADA"] = df["PK_CALZADA"].fillna("Not Available")
    # Drop NaN
    df = df[df["LOCALIDAD"].notna()]

    # Consistency
    #Convert categorical columns to appropriate data types
    df["GRAVEDAD"] = df["GRAVEDAD"].astype("category")
    df["CLASE_ACC"] = df["CLASE_ACC"].astype("category")
    df["LOCALIDAD"] = df["LOCALIDAD"].astype("category")
    #Convert FECHA_HORA_ACC to datetime
    df["FECHA_HORA_ACC"] = pd.to_datetime(df["FECHA_HORA_ACC"])
    #Rename columns with lowercase and underscore format
    columns_dict = {"OBJECTID":"id", 
                    "FORMULARIO":"form_id",
                    "CODIGO_ACCIDENTE": "accident_code",
                    "DIRECCION":"address",
                    "GRAVEDAD":"severity",
                    "CLASE_ACC":"accident_type",
                    "LOCALIDAD":"borough",
                    "FECHA_HORA_ACC":"full_date",
                    "LATITUD":"latitude",
                    "LONGITUD":"longitude",
                    "CIV":"civ",
                    "PK_CALZADA":"road_id",
                }
    df = df.rename(columns = columns_dict)
    #severity column categories
    rename_dict_severity = {"SOLO DANOS": "Only damages", "CON HERIDOS":"With Injured", "CON MUERTOS":"With deceased"}
    df["severity"] = df["severity"].cat.rename_categories(rename_dict_severity)
    #severity column categories
    rename_dict_acctype = {"ATROPELLO":"Run-over", "AUTOLESION":"Self-harm",
                            "CAIDA DE OCUPANTE":"Passenger falling", "CHOQUE":"Crash", 
                            "INCENDIO":"Fire","OTRO":"Other", "VOLCAMIENTO":"Overturn"}
    df["accident_type"] = df["accident_type"].cat.rename_categories(rename_dict_acctype)
    #borough column categories (Antonio Nari??o)
    rename_dict_boroughs = {"ANTONIO NARINO": "ANTONIO NARI??O"}
    df["borough"] = df["borough"].cat.rename_categories(rename_dict_boroughs)
    
    # Data Augmentation
    #We extract the year, month, day name, and hour from the "date" column and store them in separate columns
    df['date'] = df['full_date'].dt.date
    df["year"] = df["full_date"].dt.year
    df["month"] = df["full_date"].dt.month_name()
    mon = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df['month']= pd.Categorical(df['month'], categories=mon, ordered=True)
    df["day_of_week"] = df["full_date"].dt.day_name()
    dow = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=dow, ordered=True)
    df["hour"] = df["full_date"].dt.hour
    df["month_year"] = df["month"].astype(str).str[:3] + ", " + df["year"].astype(str)
    ## MM/YYYY
    df['Count'] = 1
    df['MM_YYYY'] = df['full_date'].dt.to_period('M').dt.strftime('%b/%Y')
    # Month, week and day number of the year
    df['month_number'] = df['full_date'].dt.month
    df['week_number'] = df['full_date'].dt.isocalendar().week
    df['day_number']= df['full_date'].dt.dayofyear

    # Loading the shape file for Bogot?? polygons of boroughs
    shp_df = gpd.read_file('data/localidades/localidades.shp')
    # Cleaning the dataframe before merging
    shp_df = shp_df.drop(["OBJECTID","CODIGO_LOC","DECRETO","LINK","SIMBOLO","ESCALA_CAP","FECHA_CAPT", "SHAPE_LEN"], axis=1)
    geo_columns_dict = {"NOMBRE":"borough", "SHAPE_AREA":"shape_area"}
    shp_df = shp_df.rename(columns = geo_columns_dict)

    #Merging accident counts and shapefile
    df_borough = df.groupby("borough")['year'].count().reset_index(name="accident_count")
    geospatial_df = shp_df.merge(df_borough, how="left", left_on=['borough'], right_on=['borough'])

    return df, geospatial_df