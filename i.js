function colonies(input1, input2) {
    a = [];
    const total = input1 + input2;
    for (let i = 1; i <= total; i++) {
        a.push(i);
    }
    const min = 1;
    var fn = function(n, src, got, all) {
        if (n == 0) {
            if (got.length > 0) {
                all[all.length] = got;
            }
            return;
        }
        for (var j = 0; j < src.length; j++) {
            fn(n - 1, src.slice(j + 1), got.concat([src[j]]), all);
        }
        return;
    }
    var all = [];
    for (var i = min; i < a.length; i++) {
        fn(i, a, [], all);
    }
    all.push(a);
    return all.length;
}


colonies(2,2);
