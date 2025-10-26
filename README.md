# Spark Sedona Spatial Joins in Cloudera Data Engineering



## CDE Setups

Create CDE Files Resource and upload scripts and data

```
cde resource create --type files \
  --name artifacts

cde resource upload --name artifacts \
  --local-path code/spatial_joins.py \
  --local-path data/las_vegas_accidents.csv \
  --local-path data/las_vegas_customer_pii.csv \
  --local-path data/las_vegas_neighborhoods.csv \
  --local-path data/las_vegas_pois.csv \
  --local-path data/las_vegas_streets.csv
```

Create CDE Python Resource

```
cde resource create --type python-env \
  --name sedona

cde resource upload --name sedona \
  --local-path resources/requirements.txt
```

## CDE Spark Connect Docker Container Setups

The demo is containerized.

#### Optional: Create the Docker Image

If you don't want to create the image and are ok just pulling one from DockerHub you can skip ahead to the next step.

Image build:

```
docker build -t pauldefusco/cde_spark_sedona_spatial_joins:latest
```

Image push:

```
docker push pauldefusco/cde_spark_sedona_spatial_joins:latest
```

#### Pull the Docker Container and Launch the IDE

Clone the GitHub repository in your local machine.

```
git clone https://github.com/pdefusco/CDE_Spark_Sedona_Spatial_Joins.git
cd CDE_Spark_Sedona_Spatial_Joins
```

Launch the Docker container.

```
docker run -p 8888:8888 pauldefusco/cde_spark_sedona_spatial_joins
```

Launch the JupyterLab IDE in your browser by copy and pasting the provided url as shown below.

![alt text](/img/docker-container-launch.png)

You now have access to all lab materials from the JupyterLab IDE in the left pane. From here, you can launch notebooks and run the terminal.

![alt text](/img/jl-home.png)

You will use the terminal in the IDE to run the CDE CLI commands for the labs. First you need to configure the CLI and install Spark Connect though.

#### Configure the CDE CLI and Install Spark Connect for CDE.

Open CDE's configurations and apply your Workload Username and Jobs API URL. You can find your Jobs API URL in your Virtual Cluster's Details Page.

![alt text](/img/jobs-api-url-1.png)

![alt text](/img/jobs-api-url-2.png)

![alt text](/img/cli-configs-1.png)

![alt text](/img/cli-configs-2.png)

Next, generate a CDP access token and edit your CDP credentials.

![alt text](/img/usr-mgt-1.png)

![alt text](/img/usr-mgt-2.png)

![alt text](/img/usr-mgt-3.png)

![alt text](/img/cdp-credentials.png)

Finally, run the following commands to install the CDE Spark Connect tarballs.

```
pip3 install cdeconnect.tar.gz  
pip3 install pyspark-3.5.1.tar.gz
```

![alt text](/img/install-deps.png)

#### Launch a CDE Spark Connect Session

Start a CDE Session of type Spark Connect. Edit the Session Name parameter so it doesn't collide with other users' sessions. You will be prompted for your Workload Password. This is the same password you used to log into CDP.

```
cde session create \
  --name geospatial-session \
  --type spark-connect \
  --num-executors 2 \
  --driver-cores 2 \
  --driver-memory "4g" \
  --executor-cores 4 \
  --executor-memory "8g"
```

![alt text](/img/launchsess.png)

In the Sessions UI, validate the Session is Running.

![alt text](/img/cde_session_validate_1.png)

![alt text](/img/cde_session_validate_2.png)

#### Run Your First PySpark & Iceberg Application via Spark Connect

You are now ready to connect to the CDE Session from your local JupyterLab IDE using Spark Connect.

Open Iceberg_TimeTravel_PySpark.ipynb. Update the Spark Connect session name, the username and the Storage Location variables in the first two cells. Then run each cell in the notebook.

```
from cde import CDESparkConnectSession
spark = CDESparkConnectSession.builder.sessionName('<your-spark-connect-session-name-here>').get()
```

```
storageLocation = <your-storage-location-here>
username = <your-cdp-workload-username-here>
```

![alt text](/img/runnotebook-1.png)
