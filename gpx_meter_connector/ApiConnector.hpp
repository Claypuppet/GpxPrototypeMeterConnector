#ifndef GPX_METER_CONNECTOR_GPX_METER_CONNECTOR_APICONNECTOR_HPP_
#define GPX_METER_CONNECTOR_GPX_METER_CONNECTOR_APICONNECTOR_HPP_

class ApiConnector {
 public:
  ApiConnector();
  ~ApiConnector() = default;

  void connect();
  bool sendData(const String& data);

 private:
};

#endif //GPX_METER_CONNECTOR_GPX_METER_CONNECTOR_APICONNECTOR_HPP_
