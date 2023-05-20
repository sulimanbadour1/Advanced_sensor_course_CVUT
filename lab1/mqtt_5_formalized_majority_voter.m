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

        % we will work with the data in an array
        A = [temperature_1 ; temperature_2 ;temperature_3]';

        % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
        % Formalized majority voter
        % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
        threshold = 0.5;

        % create sets
        % 
        for j = 1 : size(A,2)
            for k = 1: size(A,2)
                if ( abs (A(j) - A(k)) < threshold )
                    sets(j,k) = A(k);
                else
                    sets(j,k) = 0;
                end
            end
        end
       % Number of nonzero matrix elements
       count_of_non_zeros = sum(sets~=0,2)
      %   find row that has maximal number of samples < threshold
       [M,I] = max(count_of_non_zeros); 
      % from row I select randomly the sample
      % make sure to eliminate 0 elements
      idx=randperm(length(sets(I,:)),1);
      while (sets(I,idx) == 0)
           % if this element is 0 select another
           idx=randperm(length(sets(I,:)),1);
      end
      output = sets(I,idx)
      
      %   plot voting results
      %   use the same color as selected input
%       subplot(2,1,2)
      
      switch idx
        case 1
            plot(i,output,'k*')
        case 2
            plot(i,output,'m*')
        case 3
            plot(i,output,'r*')
%         case 4
%             plot(i,output,'g*')
%         case 5
%             plot(i,output,'b*')
        end
       
%       drawnow  % update plot now


    end

   drawnow
   %    pause 1 second
   pause(1)

end


% Close the connection to MQTT client by removing variable from the workspace.
unsubscribe(mqttClient)
clear mqClient