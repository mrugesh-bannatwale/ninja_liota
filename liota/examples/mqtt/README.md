# Using MQTT as Transport in LIOTA

LIOTA offers MQTT protocol as transport at both Device & DCC ends via [MqttDeviceComms](https://github.com/vmware/liota/blob/master/liota/device_comms/mqtt_device_comms.py) & [MqttDccComms](https://github.com/vmware/liota/blob/master/liota/dcc_comms/mqtt_dcc_comms.py).


## QoS
LIOTA also supports configuration of QoS related parameters like in_flight size, queue_size and retry timeout using **QoSDetails class**.


## Using MqttDeviceComms

For both ProjectICE & non-ProjectICE use-cases, MQTT related parameters required in `publish()` and `subscribe()` like topic, qos, etc., are fetched directly from the user's
configuration file.  Please refer this [example](https://github.com/vmware/liota/blob/master/examples/mqtt/device_comms/iotcc/iotcc_simulated_mqtt.py) for detailed explanation.


## Using MqttDccComms

MqttDccComms provides the flexibility of having a single topic (auto-generated or from configuration file) per MQTT connection or individual topic per metric.
**MqttMessagingAttributes class** in [mqtt.py](https://github.com/vmware/liota/blob/master/liota/lib/transports/mqtt.py) provides this flexibility.

### MqttMessagingAttributes

#### Default Values:

* Publish and Subscribe topics will be **None**
* Publish and Subscribe QoS will be **One**
* Publish retain flag will be **False** and
* Subscribe call_back will be **None**

MqttMessagingAttributes enables the following options for developers in LIOTA.

**(a)** Use single publish and subscribe topic generated by LIOTA for an EdgeSystem, its Devices and its Metrics. Default values in this case are:
* Publish topic for all Metrics will be **liota/generated_local_uuid_of_edge_system/request**
* Subscribe topic will be **liota/generated_local_uuid_of_edge_system/response**

**(b)** Use custom single publish and subscribe topic for an EdgeSystem, its Devices and Metrics.  Along with custom topics, other parameters (QoS, retain_flag ,etc.,)
can be referred from [Property File](https://github.com/vmware/liota/blob/master/examples/mqtt/dcc_comms/aws_iot/sampleProp.conf).

**-** In the above two cases, MQTT message's payload MUST be self-descriptive so that subscriber can subscribe process accordingly to a single topic by parsing payload. i.e., Along with stats of metric, its edge_system's_name, device's_name will also be appended with the payload.

**(c)** Use custom publish and subscribe topics for Metrics.

**-** In this case, MQTT message's payload need not be self-descriptive.  Subscribers can subscribe to appropriate topics accordingly.

**(d)** Use combination of **(a) and (c)** or **(b) and (c)**.


**NOTE:**
If **Option (a)** is used, `generated_local_uuid_of_edge_system` will be written to a file available at path **uuid_path** as specified in ![liota.conf](/config/liota.conf) file.
Users can refer this file to get the uuid for subscribing.


Configuring MqttDccComms and MessagingAttributes for ProjectICE and non-ProjectICE related use-cases is explained in the following sections.

### Configuration for Project ICE Scenario
[IoTCC DCC](https://github.com/vmware/liota/blob/master/liota/dccs/iotcc.py) supports both WebSockets and MQTT as transports.  It allows plug-and-play approach to easily switch between these two protocols.  However, for MQTT
it follows `Option (a)` as mentioned in the above section.
* **Option (a)** could be achieved by passing **mqtt_msg_attr=None while initializing MqttDccComms**.


### Configuration for Non-Project ICE Scenario

* **enclose_metadata** flag in [AWSIoT DCC](https://github.com/vmware/liota/blob/master/liota/dccs/aws_iot.py) can be used to specify whether a payload should be self-descriptive or not. i.e., If set to **True**, EdgeSystemName and DeviceName for a Metric will be appended
along with the payload every-time when it is published.  This is because:

  **-** If **automatic topic generation** option is used, subscribers can differentiate between metrics from different EdgeSystems & Devices by parsing the payload.  So, **enclose_metadata=True** should be used in this case.

  **-** If **custom topic per metric** option is used, subscribers can differentiate between metrics from different EdgeSystems & Devices by subscribing to appropriate topics.

* **Option (b)** could be achieved by passing **custom MqttMessagingAttributes object** while initializing **MqttDccComms**.
* **Option (c)** could be achieved by passing **custom MqttMessagingAttributes object** as an attribute with name **msg_attr** to the corresponding **RegisteredMetricObjects**

**NOTE:** MqttMessagingAttributes for a RegisteredMetric object MUST always be passed via **msg_attr** attribute of that RegisteredMetric Object.

Similarly, other DCCs can also use this approach to publish metric stats using MQTT.

Refer:
* [aws_auto_gen](https://github.com/vmware/liota/blob/master/examples/mqtt/dcc_comms/aws_iot/simulated_home_auto_gen_topic.py) example to publish to AWSIoT using **Option (a)**.
* [aws_topic_per_metric](https://github.com/vmware/liota/blob/master/examples/mqtt/dcc_comms/aws_iot/simulated_home_auto_gen_topic.py) example to publish to AWSIoT using combination of **Options (b) & (c)**.
