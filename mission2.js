var rate_a, rate_b, rate_c, rate_max;
var flag_a, flag_b, flag_c; //stock flag

flag_a = 0; flag_b = 0; flag_c = 0;

for(var t = 0; t < T; t++){
    rate_a = quote(A,t+1) / quote(A, t);
    rate_b = quote(B,t+1) / quote(B, t);
    rate_c = quote(C,t+1) / quote(C, t);
    rate_max = Math.max(rate_a, rate_b, rate_c);

    if(rate_max < 1){
        if(flag_a){
            sell(A,t);
            flag_a = 0;
        }
        if(flag_b){
            sell(B,t);
            flag_b = 0;
        }
        if(flag_c){
            sell(C,t);
            flag_c = 0;
        }
        continue;
    }

    if(rate_max == rate_a){
        if(!flag_a){
            if(flag_b){
                sell(B,t);
                flag_b = 0;
            }
            if(flag_c){
                sell(C,t);
                flag_c = 0;
            }
            buy(A,t);
            flag_a = 1;
        }
    } else if(rate_max == rate_b){
        if(!flag_b){
            if(flag_a){
                sell(A,t);
                flag_a = 0;
            }
            if(flag_c){
                sell(C,t);
                flag_c = 0;
            }
            buy(B,t);
            flag_b = 1;
        }
    } else if(rate_max == rate_c){
        if(!flag_c){
            if(flag_b){
                sell(B,t);
                flag_b = 0;
            }
            if(flag_a){
                sell(A,t);
                flag_a = 0;
            }
            buy(C,t);
            flag_c = 1;
        }
    }
}
