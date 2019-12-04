$("#street").change(function () {
    var val = $(this).val();
    switch (val) {
        case '-':
            $('#community').empty();
            $('#community').append('<option value="-">-</option>');
            break;
        case '100':
            $('#community').empty();
            $('#community').append('<option value="10002">汤坑社区</option>' +
                '<option value="10009">碧岭社区</option>' +
                '<option value="10010">沙湖社区</option>');
            break;
        case '101':
            $('#community').empty();
            $('#community').append('<option value="10013">竹坑社区</option>' +
                '<option value="10014">老坑社区</option>' +
                '<option value="10018">南布社区</option>' +
                '<option value="10020">龙田社区</option>');
            break;
        case '102':
            $('#community').empty();
            $('#community').append('<option value="10000">马峦社区</option>' +
                '<option value="10003">江岭社区</option>' +
                '<option value="10004">坪环社区</option>' +
                '<option value="10006">沙坣社区</option>');
            break;
        case '103':
            $('#community').empty();
            $('#community').append('<option value="10001">金龟社区</option>' +
                '<option value="10008">田头社区</option>' +
                '<option value="10011">田心社区</option>' +
                '<option value="10017">石井社区</option>');
            break;
        case '104':
            $('#community').empty();
            $('#community').append('<option value="10005">坪山社区</option>' +
                '<option value="10007">六联社区</option>' +
                '<option value="10012">六和社区</option>' +
                '<option value="10016">和平社区</option>');
            break;
        case '105':
            $('#community').empty();
            $('#community').append('<option value="10015">坑梓社区</option>' +
                '<option value="10019">金沙社区</option>' +
                '<option value="10021">沙田社区</option>' +
                '<option value="10022">秀新社区</option>');
            break;


    }
})