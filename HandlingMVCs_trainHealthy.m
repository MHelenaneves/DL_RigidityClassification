%% Load data

for i = 1:9
    sub{i} = load(sprintf('SUB0%d_cut_filtered.mat', i));
end

fs=2000;
% {"data": (emg, someMVCsremoved, filtered, time_cut)}
%we work with the filtered emg
%% Check plots no cuts not filtered

for i = 1:9
    figure()
    y=cell2mat(sub{i}.data(1));
    x=linspace(0,length(y),length(y));
    plot(x,y)
    xlabel('Time(s)')
    ylabel('EMG (mV)')
    title(sprintf("Subject %i",i ))
end

%% Check plots filtered data

for i = 1:9
    figure()
    y=cell2mat(sub{i}.data(3));
    x=linspace(0,length(y),length(y));
    plot(x,y)
    xlabel('Time(s)')
    ylabel('Normalized EMG (mV)')
    title(sprintf("Subject %i",i ))
end

%% Split MVCs

%sub7, 8 and 9 only have 1 MVC
%sub1 and 4 removed 2min50s beginning and end

%nMVCs=[3;4;4;3;2;4;1;1;1];
for i=1:6
    
    index1= (60*3)*fs; %cut emg after 3min from beginning
    data=cell2mat(sub{i}.data(3)); 
    
    if (i==1) || (i==4)
         
        firstMVC{i}=data(1:index1);
        secondMVC{i}=data((index1+1):(2*index1));
        thirdMVC{i}=data((2*index1+1):end);
        
    elseif (i==2) || (i==3) || (i==6)
        firstMVC{i}=data(1:index1);
        secondMVC{i}=data((index1+1):(2*index1));
        thirdMVC{i}=data((2*index1+1):(3*index1));
        fourthMVC{i}=data((3*index1+1):end);
    
    elseif i==5
        
        firstMVC{i}=data(1:index1);
        secondMVC{i}=data((index1+1):end);
        
    end
end

%% Plot splitted first MVCs

for i = 1:6
    figure()
    y=firstMVC{1,i};
    x=linspace(0,length(y),length(y));
    plot(x,y)
    xlabel('Time(s)')
    ylabel('Normalized EMG (mV)')
    title(sprintf("First MVC Subject %i",i ))
    
end
%% Plot splitted second MVCs

for i = 1:6
    figure()
    y2=secondMVC{i};
    x2=linspace(0,length(y2),length(y2));
    plot(x2,y2)
    xlabel('Time(s)')
    ylabel('Normalized EMG (mV)')
    title(sprintf("	Second MVC Subject %i",i ))
end

%% Plot splitted third MVCs

for i = 1:6
    figure()
    %y3=thirdMVC{i}(1:299403);
    y3=thirdMVC{i};
    x3=linspace(0,length(y3),length(y3));
    plot(x3,y3)
    xlabel('Time(s)')
    ylabel('Normalized EMG (mV)')
    title(sprintf("Third MVC Subject %i",i ))
end 
%% Plot splitted fourth MVCs

for i = 1:6
    figure()
    y4=fourthMVC{i};
    x4=linspace(0,length(y4),length(y4));
    plot(x4,y4)
    xlabel('Time(s)')
    ylabel('Normalized EMG (mV)')
    title(sprintf("Fourth MVC Subject %i",i ))
end

%% Interpolate data so that the MVCs have the same size

v=secondMVC{5};
new_fs=(length(secondMVC{1})*fs)/(length(secondMVC{5}));
x=linspace(0,length(secondMVC{5}),length(secondMVC{5}));
xq=0:(2000/new_fs):length(secondMVC{5});
MVC_interpolated_second=interp1(x,v,xq);

MVC_interpolated_third=[];
for i=1:6
    if length(thirdMVC{i})~=0
        if length(thirdMVC{i})<length(firstMVC{1})
            new_fs=(length(firstMVC{1})*fs)/(length(thirdMVC{i}));
            xq=0:(fs/new_fs):length(thirdMVC{i});
            x=linspace(0,length(thirdMVC{i}),length(thirdMVC{i}));
            v=thirdMVC{i};
            MVC_interpolated_sin=interp1(x,v,xq);
            MVC_interpolated_third=[MVC_interpolated_third ; MVC_interpolated_sin(1:end-1)];
        end 
    end 
end
 

MVC_interpolated_fourth=[];
for i=1:6
    if length(fourthMVC{i})~=0
        if length(fourthMVC{i}) < length(firstMVC{1})
            new_fs=(length(firstMVC{1})*fs)/(length(fourthMVC{i}));
            xq=0:(fs/new_fs):length(fourthMVC{i});
            x=linspace(0,length(fourthMVC{i}),length(fourthMVC{i}));
            v=fourthMVC{i};
            MVC_interpolated_sin=interp1(x,v,xq);
            MVC_interpolated_fourth=[MVC_interpolated_fourth ; MVC_interpolated_sin(1:end-1)];
        else
            fourthMVC{i}=fourthMVC{i};
        end
    else
        MVC_interpolated_fourth=MVC_interpolated_fourth;
    end
end

MVC_lastsub=[];
for i=7:9
    new_fs=(length(firstMVC{1})*fs)/(length(cell2mat(sub{i}.data(3))));
    xq=0:(fs/new_fs):(length(cell2mat(sub{i}.data(3))));
    v=cell2mat(sub{i}.data(3));
    x=linspace(0,(length(cell2mat(sub{i}.data(3)))),(length(cell2mat(sub{i}.data(3)))));
    MVC_interpolated_sin=interp1(x,v,xq);
    MVC_lastsub=[MVC_lastsub;MVC_interpolated_sin(1:end-1)];
end

MVC_interpolated=[MVC_interpolated_second(1:end-1);MVC_interpolated_third; MVC_interpolated_fourth; MVC_lastsub];

%% Plot interpolated

for i = 1:size(MVC_interpolated,1)
    figure()
    y4=MVC_interpolated(i,:);
    x4=linspace(0,length(y4),length(y4));
    plot(x4,y4)
    xlabel('Time(s)')
    ylabel('Normalized EMG (mV)')
    title("MVC interpolated")
end

%% 

figure()
y4=MVC_interpolated(2,:);
x4=linspace(0,length(y4),length(y4));
plot(x4,y4)
hold on
y5= thirdMVC{4};
x5=linspace(0,length(y5),length(y5));
plot(x5,y5)
ylim([min(y5) max(y5)])
xlabel('Time(s)')
ylabel('Normalized EMG (mV)')

hold off


%% Create MVC array
MVC=[];
for i=1:6
    if i==5
        MVC=[MVC; firstMVC{i}];
    else
        MVC=[MVC; firstMVC{i}; secondMVC{i}];
    end
    
    if length(thirdMVC{i})==length(firstMVC{i})
        MVC=[MVC; thirdMVC{i}];
    else
        MVC=MVC;
    end
end
MVC_six=fourthMVC{6}((length(fourthMVC{6})-length(firstMVC{1})):(end-1));

MVC=[MVC;MVC_interpolated; MVC_six];

%% Check all MVCs

for i = 1:size(MVC,1)
    figure()
    y4=MVC(i,:);
    x4=linspace(0,length(y4),length(y4));
    plot(x4,y4)
    xlabel('Time(s)')
    ylabel('Normalized EMG (mV)')
    title(sprintf(" MVC %i",i ))
end

%% EMD
for i=1:1:size(MVC,1)
    [imf{i},residual{i},info{i}] = emd(MVC(i,:));
end

%% Plot IMFs
%one plot per MVC, each plot is has 11 subplots 

fs=2000;
for i=19:(size(MVC,1))
    figure();
    %t=tiledlayout((size(MVC,1))+1,1)
    for p=1:(size(imf{i},2)+1) %1 to 10
        
        t = (0:length(MVC(i,:))-1)/fs;
        
        subplot((size(imf{i},2)+1),1, p)
        
        if p <=size(imf{i},2)
            plot(t, imf{i}(:,p));
            ylabel(sprintf("IMF %d",p ))
            hold on
        else
            plot(t,residual{i});
            ylabel("Residual")
            
        end

    end
    
    hold off
    %xlabel('Time (s)')
    %ylabel(t,'Mode Amplitude')
    %title(t,sprintf(" EMD MVC %i",i ))
end

%% Combine IMFs

emd_trainHealthy=[];
for i=1:length(imf)
    trainHealthy_emd=transpose(imf{i}(:,[6,7,8]));
    emd_trainHealthy=cat(3, trainHealthy_emd, emd_trainHealthy);
end

%% Save emd file

save ("trainhealthy.mat","emd_trainHealthy")