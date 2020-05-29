ul = document.querySelector(".content");

for (i in title) {
    li = document.createElement("li");
    li.innerHtml = i;
    ul.appendChild(li);
}
