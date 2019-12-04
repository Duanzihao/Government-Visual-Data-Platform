$("#name_left").append(profile['name']);
$("#name").val(profile['name']);
if (profile['sex'] === '男') {
    $("#sex").find("option[value='男']").attr("selected", true);
} else if (profile['sex'] === '女') {
    $("#sex").find("option[value='女']").attr("selected", true);
} else {
    $("#sex").find("option[value='-']").attr("selected", true);
}
$("#tel").val(profile['tel']);
$("#email").val(profile['email']);
$("#address").val(profile['address']);
$("#description").val(profile['description']);
$("#description_left").append(profile['description']);