%% Load healthy test data

% {"data": (emg, filtered)}
for i = 1:33
    if i==29
        sub=sub;
    else
        sub{i} = load(sprintf('SUB%d_PARAGIT_cut_filtered.mat', i));
    end
end

fs=2000;
%% Check plots no cuts not filtered

for i = 1:33
    if i==29
        sub=sub;
    else
        figure()
        y=sub{i}.data(1,:);
        x=linspace(0,length(y),length(y));
        plot(x,y)
        xlabel('Time(s)')
        ylabel('EMG (mV)')
        title(sprintf("Subject %i",i ))
    end
end

%% Check plots filtered data

for i = 1:33
    if i==29
        sub=sub;
    else
        figure()
        y=sub{i}.data(2,:);
        x=linspace(0,length(y),length(y));
        plot(x,y)
        xlabel('Time(s)')
        ylabel('Normalized EMG (mV)')
        title(sprintf("Subject %i",i ))
    end
end

%% Choose MVCs

good=[6;17;20;28;33];

%testPD=[];
for i=1:length(good)
    testPD{i}=sub{good(i)}.data(2,:);
end

%% Transform to the final size

MVC_size=360000;

for i=1:length(testPD)
    n=ceil(length(testPD{i})/MVC_size);
    testPD_downsample{i}=downsample(testPD{i},n);
end
 
testPD_interpolated=[];
for i=1:length(testPD)
    if length(testPD_downsample{i})< MVC_size
        new_fs=(MVC_size*fs)/length(testPD_downsample{i});
        xq=0:(fs/new_fs):length(testPD_downsample{i});
        x=linspace(0,length(testPD_downsample{i}),length(testPD_downsample{i}));
        v=testPD_downsample{i};
        testPD_interpolated_sin=interp1(x,v,xq);
        testPD_interpolated=[testPD_interpolated; testPD_interpolated_sin(1:MVC_size)];
    end
end

%% Plot interpolated

for i = 1:size(testPD_interpolated,1)
    figure()
    y4=testPD_interpolated(i,:);
    x4=linspace(0,length(y4),length(y4));
    plot(x4,y4)
    xlabel('Time(s)')
    ylabel('Normalized EMG (mV)')
    title("MVC interpolated")
end

%% EMD
for i=1:1:size(testPD_interpolated,1)
    [imf{i},residual{i},info{i}] = emd(testPD_interpolated(i,:));
end

%% Plot IMFs
%one plot per MVC, each plot is has 11 subplots 

fs=2000;
for i=1:(size(testPD_interpolated,1))
    figure();
    for p=1:(size(imf{i},2)+1) %1 to 10
        
        t = (0:length(testPD_interpolated(i,:))-1)/fs;

        subplot((size(imf{i},2)+1),1, p)
        
        if p <=size(imf{i},2)
            plot(t, imf{i}(:,p));
            hold on
        else
            plot(t,residual{i}); 
        end
    end
    hold off
end

%% Combine IMFs

emd_testPD=[];
for i=1:length(imf)
    testPD_emd=transpose(imf{i}(:,[6,7,8]));
    emd_testPD=cat(3, testPD_emd,emd_testPD);
end

%% Save emd file

save ("testPD.mat","emd_testPD")
