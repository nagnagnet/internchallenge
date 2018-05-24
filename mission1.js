var flag = 0; // stock flag
for(var t = 0; t < T; t++){
    if(quote(A, t) < quote(A, t+1)){
        if(!flag){
            buy(A,t);
            flag = 1;
        }
    } else {
        if(flag){
            sell(A,t);
            flag = 0;
        }
    }
}