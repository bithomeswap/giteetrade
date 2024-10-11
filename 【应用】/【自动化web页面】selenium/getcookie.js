// 这个是有bug的，就是定义了一个cookie，再打印出来，执行的时候直接命令行输入 node 文件路径 即可
// function getCookies() {
//     let cookie = "username=geeks;expires=Mon, 18 Dec 2023;path=/";
//     let cookies = cookie.split(';').reduce(
//         (cookies, cookie) => {
//             const [name, val] = cookie.split('=').map(c => c.trim());
//             cookies[name] = val;
//             return cookies;
//         }, {});
//     return cookies;
// }
// console.log(getCookies());


//浏览器网址搜索栏手动输入下面的代码【目的是防泄露】，或许模拟人工输入也可以
javascript:alert(document.cookie)