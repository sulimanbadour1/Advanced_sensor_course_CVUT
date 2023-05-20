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

% init
temperature_1_previous = 0;
temperature_2_previous = 0;
temperature_3_previous = 0;


% read n samples, line by line
for i = 1: get_n_samples
     
    % returns the most recent message from all subscribed topics for the specified MQTT client, as a timetable of messages
    mqttMsg = peek(mqttClient,Topic=topicToSub)

    % extract data from table
    % only if we have all 3 temperatures
    if length(mqttMsg.Data) >= 3
        temperature_1 = str2num(mqttMsg.Data(1));
        temperature_2 = str2num(mqttMsg.Data(2));
        temperature_3 = str2num(mqttMsg.Data(3));

        % we will work with the data in an array
        A = [temperature_1 ; temperature_2 ;temperature_3]';

        % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
        % calculate median
        % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
        M = median (A)

        % calculate distance of each from median
        temperature_1_delta_from_median = temperature_1 - M
        temperature_2_delta_from_median = temperature_2 - M
        temperature_3_delta_from_median = temperature_3 - M

        % chosen value for amplitude threshold
        amplitude_threshold = 0.5;

        % verify for fault
        % Amplitude threshold detector        
        if temperature_1_delta_from_median > amplitude_threshold
            disp("Amplitude threshold detector warning - possible fault on temperature 1 - value to far from mean")
        end

        if temperature_2_delta_from_median > amplitude_threshold
            disp("Amplitude threshold detector warning - possible fault on temperature 2 - value to far from mean")
        end

        if temperature_3_delta_from_median > amplitude_threshold
            disp("Amplitude threshold detector warning - possible fault on temperature 3 - value to far from mean")
        end


        % chosen value for amplitude threshold
        time_threshold = 0.5;

        % verify for fault
        % Time threshold detector   

        % calculate time delta
        temperature_1_time_delta = temperature_1 - temperature_1_previous
        temperature_2_time_delta = temperature_2 - temperature_2_previous
        temperature_3_time_delta = temperature_3 - temperature_3_previous

        temperature_1_previous = temperature_1;
        temperature_2_previous = temperature_2;
        temperature_3_previous = temperature_3;

        if temperature_1_time_delta > time_threshold
            disp("Time threshold detector warning - possible fault on temperature 1 - delta too large")
        end

        if temperature_2_time_delta > time_threshold
            disp("Time threshold detector warning - possible fault on temperature 2 - delta too large")
        end

        if temperature_3_time_delta > time_threshold
            disp("Time threshold detector warning - possible fault on temperature 3 - delta too large")
        end


        plot(i,temperature_1,'k*')
        plot(i,temperature_2,'g*')
        plot(i,temperature_3,'b*')
        plot(i,M,'r*')
        legend('temperature 1','temperature 2','temperature 3', 'median')

        drawnow

    end

   %    pause 1 second
   pause(1)

end


% Close the connection to MQTT client by removing variable from the workspace.
unsubscribe(mqttClient)
clear mqClient