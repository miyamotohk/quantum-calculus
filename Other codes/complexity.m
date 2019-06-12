clear all

%% Shor's algorithm
% Shor ciruit
n1 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19];
nG1 = [998, 2914, 6822, 13802, 25174, 42498, 67574, 102442, 149382, 210914, 289798, 389034, 511862, 661762, 842454, 1057898, 1312294];
fit1 = fit(n1', nG1', 'poly4')

figure(1);
title('Number of gates of complete Shor circuit')
hold on;
scatter(n1,nG1)
plot(fit1);
xlabel('n');
ylabel('Number of gates')
hold off;


% Ua gate
N2 = [7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191, 16383, 32767, 65535, 131071, 262143, 524287];
nG2 = [378, 700, 1172, 1824, 2686, 3788, 5160, 6832, 8834, 11196, 13948, 17120, 20742, 24844, 29456, 34608, 40330];
n2 = ceil(log2(N2));
fit2 = fit(n2', nG2', 'poly3')

figure(2);
title('Number of gates of gate Ua circuit')
hold on;
scatter(n2,nG2)
plot(fit2);
xlabel('n');
ylabel('Number of gates')
hold off;

% CMULT gate
N3 = [7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191, 16383, 32767, 65535, 131071, 262143, 524287];
nG3 = [200, 363, 601, 929, 1362, 1915, 2603, 3441, 4444, 5627, 7005, 8593, 10406, 12459, 14767, 17345, 20208];
n3 = ceil(log2(N2));
fit3 = fit(n3', nG3', 'poly3')

figure(3);
title('Number of gates of CMULT circuit')
hold on;
scatter(n3,nG3)
plot(fit3);
xlabel('n');
ylabel('Number of gates')
hold off;

%% Probability distributions
n4 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
nG4 = [1343, 3180, 6490, 11905, 20205, 32374, 49238, 72193, 102262, 140821];
fit4 = fit(n4', nG4', 'poly4')

figure(4);
title('Number of gates of approximate arcsin circuit')
hold on;
scatter(n4,nG4)
plot(fit4);
xlabel('n');
ylabel('Number of gates')
hold off;