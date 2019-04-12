# SampleWebService


This repository contains code for sample web service, which given number N as input, returns first N Fibonacci numbers. As this project is just for demonstration purposes, I'm using Flask micro-framework to provide the service. Service is provided at <code>/fibseq</code> endpoint.

To ease the deployment, service is to be built as a Docker image. Besides it's main functionality, service also provides simple metrics to Prometheus and also logs it's errors to file.

<h2>Build</h2>

Start build process by cloning this repository first:
<code>git clone https://github.com/mariusm-sec/SampleWebService.git</code>

Then change to a newly created directory: <code>cd SampleWebService</code>. All further actions are to be done from this directory, unless stated otherwise. Directory contains various configuration/build files and <code>src/</code> sub-directory, which contains all application related code. 

Start with building Flask application first: 

<code>docker build -t fib_service .</code> 

As application exports metrics for Prometheus, we are going to run <code>fib_service</code> application together with Prometheus server. If such a server is already present in your environment, you can adjust <code>docker-compose.yml</code> file accordingly and remove Prometheus part. In that case one has to specify Prometheus' target for our new application as <code>Docker_host_IP:5000</code>, since <code>fib_service</code> application will start on port 5000.

After all configuration modifications (if any), run docker-compose: 

<code>docker-compose up -d</code>

This should start both Flask and Prometheus servers as Docker containers. Test if our application is working by issuing HTTP request: 

<code>curl -XGET http://localhost:5000/fibseq/6</code>. 

If everything is ok, a JSON object should be provided in the response, such as <code>{"error":null,"input":"6","sequence":[{"error":null,"input":"6","sequence":[0,1,1,2,3,5]}}</code>. One can see that given input 6, there was no error and resulting sequence is <code>[0,1,1,2,3,5]</code>.

If invalid input is provided, e.g., negative number, application will set <code>error</code> in response to some non-null value. E.g., 

<code>curl -XGET http://localhost:5000/fibseq/-5</code>

will return

<code>
{"error":"Negative value, service accepts only non-negative numbers","input":"-5","sequence":null}
</code>

<h2>Logging</h2>

Application uses Flask's logger to write log file in the <code>logs</code> directory. This directory is a Docker volume, mounted to a container. Application code in <code>src/fib_app.py</code> is responsible for logger setup. Application warnings and/or errors will be written to <code>logs/flask.log</code> file. All requests to Flask will be also visible on Flask's stdout. These logs may be accessed by <code>docker logs fib_service</code> (assuming that container is up and running).

<h2>Testing</h2>
<code>src/test_fibapp.py</code> provides unit tests. One part tests <code>fib.py</code> module's functionality. Second one tests Flask's application. It doesn't require application to be running, as it uses Flask's test client to serve HTTP requests. One may run these tests either via <code>python src/test_fibapp.py</code> or, if <code>py.test</code> is available - <code>cd src; py.test -v</code>.

<h2>Metrics</h2>
Application exports metrics, which are to be collected by Prometheus server. Number of requests and request latency are recorded and can be collected at <code>/metrics</code> endpoint: <code>curl -XGET http://localhost:5000/metrics</code>. Metrics are setup in such a way that every request is recorded, including requests for metrics itself.

In order to see the recorded metrics, one should open Prometheus in his browser (http://localhost:9090, if Prometheus has been started via <code>docker-compose</code>). One should see metrics such as flask_prometheus_request_latency* or flask_prometheus_request_count*.
