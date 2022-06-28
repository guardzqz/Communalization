window.onload=function(){
    initColor();
}
function initColor(){
    var cnt = document.getElementsByClassName('roww');//找到元素
    for (var k=0; k<cnt.length; k++){
        change_color(k);
    }
}
function sty(id){
    change_color(id-1);
}
function change_color(id){
    var cnt = document.getElementsByClassName('roww');//找到元素
    for (var i=0;i<cnt[id].children[1].children.length;i++){
        if (cnt[id].children[1].children[i].checked) {
            if (cnt[id].children[1].children[i].value=='no') {
                cnt[id].parentNode.style.backgroundColor="#CD5C5C";
            }
            else if (cnt[id].children[1].children[i].value=='yes') {
                cnt[id].parentNode.style.backgroundColor="#548B54";
            }
            else{
                cnt[id].parentNode.style.backgroundColor="lightgray";
            }
        }
    }
}

function resultBtn(){
    var d1 = '<!DOCTYPE html><html lang="en">';
    var heads = document.getElementsByTagName("head")[0];
    d1 += heads.outerHTML;
    d1 += '<body><h1>用例结果</h1><div class="contain-all">';
    var count = document.getElementsByClassName('contain-row');
    for (var j=0;j<count.length;j++){
        d1 += '<div class="contain-row"><div class="case-index roww" onclick="sty('+(j+1)+')"><p>'+(j+1)+'</p><p>';
        var tags = document.getElementsByName(j+1);
        var operation = ['未操作', '通过', '未通过'];
        for (var i=0;i<tags.length;i++){
            if (tags[i].checked){
                d1 += '<br><input type="radio" name='+(j+1)+' value="'+tags[i].value+'" id="'+tags[i].value+(j+1)+'" checked><label for="'+tags[i].value+(j+1)+'">'+operation[i]+'</label>';
            }
            else{
                d1 += '<br><input type="radio" name='+(j+1)+' value="'+tags[i].value+'" id="'+tags[i].value+(j+1)+'"><label for="'+tags[i].value+(j+1)+'">'+operation[i]+'</label>';
            }
        }
        d1 += '<br></p></div>';
        var titles = document.getElementsByClassName('case-title')[j];
        d1 += titles.outerHTML;
        var texts = document.getElementsByClassName('case-text')[j];
        d1 += texts.outerHTML;
        var imgs = document.getElementsByClassName('imgarea')[j];
        d1 += imgs.outerHTML;
        var others = document.getElementsByClassName('atextarea')[j];
        d1 += '<div class="atextarea"><textarea>'+others.firstElementChild.value+'</textarea></div></div>';
    }
    d1 += '</div><button type="button" onclick="resultBtn()">获取最终结果</button></body></html>';
//    console.log(d1);
    var filetitle = document.getElementsByTagName('title')[0];
    var file = new File([d1], filetitle.text, {type: "text/plain;charset=utf-8"});
    saveAs(file);
}

