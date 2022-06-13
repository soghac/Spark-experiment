import os
import time
from pyspark.sql import SparkSession
from pyspark.ml.feature import RFormula


def get_spark_session(app_name: str):
    return SparkSession.builder \
        .master('spark://spark-master:7077') \
        .appName(app_name) \
        .getOrCreate()



try:
    import flask
except Exception:
    os.system('pip install flask')
    time.sleep(10)
    import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/get/', methods=['GET'])
def spark_test():
    spark = get_spark_session("test")
    try:
        path = f"/src/data/g2.csv"
        df = spark.read.csv(path, header=True)
        df.show()

        formula = RFormula(
            formula="clicked ~ country_code1 + hour",
            featuresCol="features",
            labelCol="label")

        output = formula.fit(df).transform(df)
        sample = output.select("features", "label").head(5)
        return f"<h1>Sample</h1><p>{sample}</p>"
    except Exception:
        spark.stop()
        return "<h1>Sample</h1><p>{sample}</p>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
