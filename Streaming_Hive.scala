package test
import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds,StreamingContext}

object Streaming_Hive {
  case class Record(ServerIP:String,webiste:String,Keyword:String)

  def main(args: Array[String]): Unit = {
    val batch = 10

    val conf = new SparkConf().setAppName("ScalaTest")
    val ssc = new StreamingContext(conf, Seconds(batch))

    val lines = ssc.textFileStream("hdfs:///spark/streaming/")
    //1.总PV
    lines.count().print()

    //2.各ip的pv，按pv倒序排列
    lines.map(line => (line.split(" ")(0), 1)).reduceByKey(_ + _).transform(rdd => {
      rdd.map(ip_pv => (ip_pv._2, ip_pv._1))
        .sortByKey(false).map(ip_pv => (ip_pv._2, ip_pv._1))
    }).print()

    //3.搜索引擎pv
    val refer = lines.map(_.split("\"")(3))
    val searchEngineInfo = refer.map(r => {
      val f = r.split("/")
      val searchEngine = Map(
        "www.google.cn" -> "q",
        "www.yahoo.com" -> "p",
        "cn.bing.com" -> "q",
        "www.baidu.com" -> "wd",
        "www.sogou.com" -> "query"
      )

      if (f.length > 2) {
        val host = f(2)
        if (searchEngine.contains(host)) {
          val query = r.split('?')(1)
          if (query.length > 0) {
            val arr_search_q = query.split('&').filter(_.indexOf(searchEngine(host) + "=") == 0)
            if (arr_search_q.length > 0)
              (host, arr_search_q(0).split('=')(1))
            else
              (host, "")
          } else {
            (host, "")
          }
        } else
          ("", "")
      } else
        ("", "")

    })
    //输出搜索引擎pv
    searchEngineInfo.filter(_._1.length > 0).map(p => (p._1, 1)).reduceByKey(_ + _).print()

    //输出关键词PV
    searchEngineInfo.filter(_._2.length > 0).map(p => (p._2, 1)).reduceByKey(_ + _).print()

    ssc.start()
    ssc.awaitTermination()
  }
}
