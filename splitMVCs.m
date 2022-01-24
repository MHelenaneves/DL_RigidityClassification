% If one recording has more than one MVC, splitMVCs splits the recording in
% n, with n being the number of MVCs
%only works for test set F01, F02, F03, F04 so far

%Input
%   - data: filtered emg recording, as a vector
%   - n: number of MVCs present in the recording , goes from 1 to 4
%   - cut_point: point where to split the recording, in minutes

%Output:
%   - MVC_splitted: cell array, each cell corresponds to an MVC array of
%   size index1


function [MVC, MVC_rest] = splitMVCs(data, n, cut_point) 
    fs=2000; 
    index1= (60*cut_point)*fs;
    
    for i=1:n
        MVC=data(1:index1);
        MVC_rest=data((index1+1):(end));
    end
end