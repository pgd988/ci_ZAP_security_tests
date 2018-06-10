;Before you start service you need install python libs from  requrements.txt 

;For service manage you need run ZAP_start.sh (start|stop)

;After first run you need create _scan index into Elasticsearch
;for do that run any POST app (Insomnia or Postman for example) and send this PUT request into your Elasticsearch IP:

PUT http://[your elasticsearch container listen IP here]:9200/scans/

{
  "mappings": {
    "scan": {
      "properties": {
        "alerts": {
          "type": "nested"
        }
      }
    }
  }
}

; It will create _scan index and save it into ./esdata dir. so next time when container will start, index already will be created.
;Also any data stored into elasticsearch will be automatically readed by container on every start from ./esdata dir.
;And you does not loose your data even if container will be removed.

; After you will start service by ZAP_start.sh you may run any URL scans just type:

./sacan.py [http://URL_here]

; Pay your attention you need specify http or https protocols for scan urls
; Mostly errors you may get from scan script will tell you about ZAP container is inaccessible
; if you got the error first check ZAP container ip and port settings in the script.

;After the scan is over you will see resulting message in your std.out and full report will sended to the elasticsearch container
; so you can get it by Kibana http://[your kibana container IP here ]:5601
; to be continued...

