%% Load data

for i = 1:13
    sub{i} = load(sprintf('SUB%d_FAKE_cut_filtered.mat', i));
end

fs=2000;
% {"data": (emg, filtered)}
%we work with the filtered emg
%% Check plots no cuts not filtered

for i = 1:13
    figure()
    y=sub{i}.data(1,:);
    x=linspace(0,length(y),length(y));
    plot(x,y)
    xlabel('Time(s)')
    ylabel('EMG (mV)')
    title(sprintf("Subject %i",i ))
end

%% Check plots filtered data

for i = 1:13
    figure()
    y=sub{i}.data(2,:);
    x=linspace(0,length(y),length(y));
    plot(x,y)
    xlabel('Time(s)')
    ylabel('Normalized EMG (mV)')
    title(sprintf("Subject %i",i ))
end

%% Split MVCs

%sub4 and 5 only have 1 MVC

for i=1:13
    
    index1= (60*2.3)*fs; 
    index2= (60*2.05)*fs;
    index3= (60*1.5)*fs;
    index4= (60*1)*fs;
    data=sub{i}.data(2,:);
    
    if (i==1) || (i==3) %three MVCs 
        firstMVC{i}=data(1:index1);
        secondMVC{i}=data((index1+1):(2*index1));
        thirdMVC{i}=data((2*index1+1):end);
        
    elseif (i==2) %four MVCs
        firstMVC{i}=data(1:index1);
        secondMVC{i}=data((index1+1):(index1+1+index2));
        thirdMVC{i}=data((index1+1+index2+1):(index1+1+index2+1+index3));
        fourthMVC{i}=data((index1+1+index2+1+index3+1):end);
        
    elseif (i==13) %four MVCs
        firstMVC{i}=data(1:index2);
        secondMVC{i}=data((index2+1):(2*index3));
        thirdMVC{i}=data((2*index3+1):(3*index3));
        fourthMVC{i}=data((3*index3+1):end);
        
    elseif (i==12) %three MVCs
        firstMVC{i}=data(1:index3);
        secondMVC{i}=data((index3+1):(2*index3));
        thirdMVC{i}=data((2*index3+1):end);
    
    elseif (i==10) || (i==11) %two MVCs
        
        firstMVC{i}=data(1:index2);
        secondMVC{i}=data((index2+1):end);
        
    elseif (i==9) %two MVCs
        firstMVC{i}=data(1:index3);
        secondMVC{i}=data((index3+1):end);
        
    elseif (i==4) || (i==5)
        firstMVC{i}=data;
        
    elseif (i==6) || (i==7) || (i==8) %sub6, sub7 and sub8 were excluded
        sub{i}=[];
    end
end

%% Plot splitted first MVCs

for i = 1:13
    figure()
    y=firstMVC{1,i};
    x=linspace(0,length(y),length(y));
    plot(x,y)
    xlabel('Time(s)')
    ylabel('Normalized EMG (mV)')
    title(sprintf("First MVC Subject %i",i ))
    
end
%% Plot splitted second MVCs

for i = 1:13
    figure()
    y2=secondMVC{i};
    x2=linspace(0,length(y2),length(y2));
    plot(x2,y2)
    xlabel('Time(s)')
    ylabel('Normalized EMG (mV)')
    title(sprintf("	Second MVC Subject %i",i ))
end

%% Plot splitted third MVCs

for i = 1:13
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

for i = 1:13
    figure()
    y4=fourthMVC{i};
    x4=linspace(0,length(y4),length(y4));
    plot(x4,y4)
    xlabel('Time(s)')
    ylabel('Normalized EMG (mV)')
    title(sprintf("Fourth MVC Subject %i",i ))
end

%% Interpolate data so that the MVCs have the same size

final_size=360000;

MVC_interpolated_first=[];
for i=1:13
    if length(firstMVC{i})~=0
        if length(firstMVC{i})<final_size
            new_fs=(final_size*fs)/(length(firstMVC{i}));
            xq=0:(fs/new_fs):length(firstMVC{i});
            x=linspace(0,length(firstMVC{i}),length(firstMVC{i}));
            v=firstMVC{i};
            MVC_interpolated_sin=interp1(x,v,xq);
            MVC_interpolated_first=[MVC_interpolated_first ; MVC_interpolated_sin(1:end-1)];
        end 
    end 
end
%% 

MVC_interpolated_second=[];
for i=1:13
    if length(secondMVC{i})~=0
        if length(secondMVC{i})<final_size
            new_fs=(final_size*fs)/(length(secondMVC{i}));
            xq=0:(fs/new_fs):length(secondMVC{i});
            x=linspace(0,length(secondMVC{i}),length(secondMVC{i}));
            v=secondMVC{i};
            MVC_interpolated_sin=interp1(x,v,xq);
            MVC_interpolated_second=[MVC_interpolated_second ; MVC_interpolated_sin(1:end-1)];
        end 
    end 
end


MVC_interpolated_third=[];
for i=1:13
    if length(thirdMVC{i})~=0
        if length(thirdMVC{i})<final_size
            new_fs=(final_size*fs)/(length(thirdMVC{i}));
            xq=0:(fs/new_fs):length(thirdMVC{i});
            x=linspace(0,length(thirdMVC{i}),length(thirdMVC{i}));
            v=thirdMVC{i};
            MVC_interpolated_sin=interp1(x,v,xq);
            MVC_interpolated_third=[MVC_interpolated_third ; MVC_interpolated_sin(1:end-1)];
        end 
    end 
end
 

MVC_interpolated_fourth=[];
for i=1:13
    if length(fourthMVC{i})~=0
        if length(fourthMVC{i}) < final_size
            new_fs=(final_size*fs)/(length(fourthMVC{i}));
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


MVC_interpolated=[MVC_interpolated_first;MVC_interpolated_second;MVC_interpolated_third; MVC_interpolated_fourth];

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

%% Create MVC array
MVC=[];
for i=1:size(MVC_interpolated,1)
    if (i==4) || (i==13) %MVC4 and MVC13 were excluded bc they were the worst
        MVC=MVC;
    else
        MVC=[MVC; MVC_interpolated(i,:)];
    end
end


%% Check all MVCs

for i = 1:size(MVC,1)
    figure()
    y4=MVC(i,:);
    x4=linspace(0,length(y4),length(y4));
    plot(x4,y4)
    xlabel('Time(s)')
    ylabel('Normalized EMG (mV)')
    title("MVC")
end

%% EMD
for i=1:1:size(MVC,1)
    [imf{i},residual{i},info{i}] = emd(MVC(i,:));
end

%% Plot IMFs
%one plot per MVC, each plot has 11 subplots 

fs=2000;
for i=1:(size(MVC,1))
    figure();
    for p=1:(size(imf{i},2)+1) %1 to 10
        
        t = (0:length(MVC(i,:))-1)/fs;
        
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

emd_trainPD=[];
for i=1:length(imf)
    trainPD_emd=transpose(imf{i}(:,[6,7,8]));
    emd_trainPD=cat(3, trainPD_emd, emd_trainPD);
end

%% Save emd file

save ("trainPD.mat","emd_trainPD")