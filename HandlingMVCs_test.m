%% Load healthy test data

%load('F01_cut_filtered.mat')
% {"data": (emg, someMVCsremoved, filtered)}
for i = 1:4
    sub{i} = load(sprintf('F0%d_cut_filtered.mat', i));
end

fs=2000;
%% Check plots no cuts not filtered

for i = 1:4
    figure()
    y=cell2mat(sub{i}.data(1));
    x=linspace(0,length(y),length(y));
    plot(x,y)
    xlabel('Time(s)')
    ylabel('EMG (mV)')
    title(sprintf("Subject %i",i ))
end

%% Check plots filtered data

for i = 1:4
    figure()
    y=cell2mat(sub{i}.data(3));
    x=linspace(0,length(y),length(y));
    plot(x,y)
    xlabel('Time(s)')
    ylabel('Normalized EMG (mV)')
    title(sprintf("Subject %i",i ))
end
%% Split MVCs

n_MVCs_sub=[2;1;1;1];
MVC_all={};
for i=1:4
    n=n_MVCs_sub(i);
    if n<=1
        add=sub{i}.data(3);
        MVC_all=[MVC_all add];
    else
        data=cell2mat(sub{i}.data(3));
        [splitted, MVC_rest] = splitMVCs(data, n, 1.5);
        MVC_all=[MVC_all splitted MVC_rest];
    end
end

%% Check splitted MVC

for i=1:length(MVC_all)
    figure()
    y=MVC_all{i};
    x=linspace(0,length(y),length(y));
    plot(x,y)
    xlabel('Time(s)')
    ylabel('Normalized EMG (mV)')
    title(sprintf("Splitted MVC %i",i ))
end

%% Interpolate data so that the MVCs have the same size

MVC_interpolated_test=[];
final_size=360000;
for i=1:5
    if length(MVC_all{i})~=0
        if length(MVC_all{i})<final_size
            new_fs=(final_size*fs)/length(MVC_all{i});
            xq=0:(fs/new_fs):length(MVC_all{i});
            x=linspace(0,length(MVC_all{i}),length(MVC_all{i}));
            v=MVC_all{i};
            MVC_interpolated_sin=interp1(x,v,xq);
            MVC_interpolated_test=[MVC_interpolated_test ; MVC_interpolated_sin(1:end-1)];
        end 
    end 
end
 
%% Plot interpolated

for i = 1:size(MVC_interpolated_test,1)
    figure()
    y4=MVC_interpolated_test(i,:);
    x4=linspace(0,length(y4),length(y4));
    plot(x4,y4)
    xlabel('Time(s)')
    ylabel('Normalized EMG (mV)')
    title("MVC interpolated")
end

%% EMD
for i=1:1:size(MVC_interpolated_test,1)
    [imf{i},residual{i},info{i}] = emd(MVC_interpolated_test(i,:));
end

%% Plot IMFs
%one plot per MVC, each plot is has 11 subplots 

fs=2000;
for i=1:(size(MVC_interpolated_test,1))
    figure();
    for p=1:(size(imf{i},2)+1) %1 to 10
        
        t = (0:length(MVC_interpolated_test(i,:))-1)/fs;

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

emd_testhealthy=[];
%testPD_emd=[];
for i=1:length(imf)
    testhealthy_emd=transpose(imf{i}(:,[6,7,8]));
    emd_testhealthy=cat(3, testhealthy_emd,emd_testhealthy);
end

%% Save emd file

save ("testhealthy.mat","emd_testhealthy")

