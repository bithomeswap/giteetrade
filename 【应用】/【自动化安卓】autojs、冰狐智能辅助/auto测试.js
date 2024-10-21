// 无障碍服务已启用但并未运行，这可能是安卓的BUG，您可能需要重启手机或重启无障碍服务
// 可能是因为安卓版本太新了有干扰
toast('Hello World');

// var packageName = "com.ss.android.ugc.aweme"; // 视频App的包名
// launch(packageName);// 打开视频App

// var appName = rawInput("快手极速版");// 视频App的包名
// launchApp(appName);// 打开视频App

launchApp("抖音极速版");// 打开视频App

print("打开app成功")//这里开始报错【无障碍模式已经启用但是无法执行】
waitForPackage(packageName);// 等待视频App加载完成
autoSwipe();// 自动刷视频
// 自动刷视频函数
function autoSwipe() {
  while (true) {
    // 模拟向下滑动操作
    swipe(
      device.width / 2,
      device.height * 0.8,
      device.width / 2,
      device.height * 0.2,
      1000
    );
    // 等待一段时间，模拟观看视频
    sleep(5000); // 可以根据实际情况调整等待时间
  }
}
