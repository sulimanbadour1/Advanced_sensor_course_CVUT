% this code is for Matlab 2022a and newer
% with Industrial Communication Toolbox

userName = "SNSlab";
password = "SNSlab";

% Prepare the broker address and port number you want to connect. 
brokerAddress = "tcp://141.145.219.166";
port = 1883;

mqttClient = mqttclient(brokerAddress, Port = port, ...
           Username = userName, Password = password)

% Note that the Connected property indicates the connection to the broker has been established.
mqttClient.Connected

% Subscribe to a Topic
% topicToSub = "SNS_labs/temperature_1";
% subscribe to all topics
topicToSub = "SNSlabs/+";
subscribe(mqttClient, topicToSub)


% how many samples to get from MQTT
get_n_samples = 100;

% create plot
time_plot = figure;
xlabel('sample [-]')
ylabel('temperature [°C]')
hold on
grid on
axis([1 get_n_samples 15 30])


% variance and average
% initial values
temperature_1_average_previous = 0;
temperature_2_average_previous = 0;
temperature_3_average_previous = 0;
temperature_1_variance_previous = 0;
temperature_2_variance_previous = 0;
temperature_3_variance_previous = 0;


% read n samples, line by line
for i = 1: get_n_samples
     
    % returns the most recent message from all subscribed topics for the specified MQTT client, as a timetable of messages
    mqttMsg = peek(mqttClient,Topic=topicToSub)

    % extract data from table
    % only if we have all 3 temperatures
    if length(mqttMsg.Data) >= 3
        temperature_1 = str2num(mqttMsg.Data(1))
        temperature_2 = str2num(mqttMsg.Data(2))
        temperature_3 = str2num(mqttMsg.Data(3))

        % plots
        plot(i,temperature_1,'r*');
        plot(i,temperature_2,'g*');
        plot(i,temperature_3,'b*');
        legend('temperature 1','temperature 2','temperature 3')

        %   calculations
        %   formulas lecture Sensor fusion, slide 24
        temperature_1_average = temperature_1_average_previous + (temperature_1 - temperature_1_average_previous) / i
        temperature_2_average = temperature_2_average_previous + (temperature_2 - temperature_2_average_previous) / i
        temperature_3_average = temperature_3_average_previous + (temperature_3 - temperature_3_average_previous) / i

        % start variance calculations from 2th sample
        if (i > 1)
            temperature_1_variance = (temperature_1_variance_previous ^2 + (temperature_1 - temperature_1_average) * (temperature_1 - temperature_1_average_previous)) / (i - 1)
            temperature_2_variance = (temperature_2_variance_previous ^2 + (temperature_2 - temperature_2_average) * (temperature_2 - temperature_2_average_previous)) / (i - 1)
            temperature_3_variance = (temperature_3_variance_previous ^2 + (temperature_3 - temperature_3_average) * (temperature_3 - temperature_3_average_previous)) / (i - 1)

            temperature_1_variance_previous = temperature_1_variance ;
            temperature_2_variance_previous = temperature_2_variance ;
            temperature_3_variance_previous = temperature_3_variance ;            
        end

        % store history for future calculations
        temperature_1_average_previous = temperature_1_average;
        temperature_2_average_previous = temperature_2_average;
        temperature_3_average_previous = temperature_3_average;



    end

   drawnow
   %    pause 1 second
   pause(1)

end


% Close the connection to MQTT client by removing variable from the workspace.
unsubscribe(mqttClient)
clear mqClient