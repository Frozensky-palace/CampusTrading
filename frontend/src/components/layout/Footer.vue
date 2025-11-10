<template>
  <footer class="footer">
    <div class="footer-container">
      <!-- 页脚内容区域 -->
      <div class="footer-content">
        <!-- 网站介绍 -->
        <div class="footer-about">
          <h3 class="footer-title">校园二手交易平台</h3>
          <p class="footer-description">
            为校园师生提供便捷、安全的二手商品交易服务，帮助大家实现资源共享和循环利用，共同建设绿色校园。
          </p>
          <div class="footer-social">
            <a href="#" class="social-link" title="微信公众号"><i class="el-icon-chat-line-square"></i></a>
            <a href="#" class="social-link" title="QQ群"><i class="el-icon-chat-dot-round"></i></a>
            <a href="#" class="social-link" title="微博"><i class="el-icon-share"></i></a>
          </div>
        </div>
        
        <!-- 快速链接 -->
        <div class="footer-links">
          <h3 class="footer-title">快速链接</h3>
          <ul class="link-list">
            <li><router-link to="/" class="link-item">首页</router-link></li>
            <li><router-link to="/items" class="link-item">商品列表</router-link></li>
            <li><router-link to="/requests" class="link-item">求购信息</router-link></li>
            <li><router-link to="/compare" class="link-item">比价中心</router-link></li>
            <li><router-link to="/about" class="link-item">关于我们</router-link></li>
          </ul>
        </div>
        
        <!-- 帮助中心 -->
        <div class="footer-help">
          <h3 class="footer-title">帮助中心</h3>
          <ul class="link-list">
            <li><a href="#" class="link-item">新手指南</a></li>
            <li><a href="#" class="link-item">交易规则</a></li>
            <li><a href="#" class="link-item">常见问题</a></li>
            <li><a href="#" class="link-item">用户反馈</a></li>
            <li><a href="#" class="link-item">联系客服</a></li>
          </ul>
        </div>
        
        <!-- 联系我们 -->
        <div class="footer-contact">
          <h3 class="footer-title">联系我们</h3>
          <ul class="contact-list">
            <li class="contact-item">
              <i class="el-icon-location"></i>
              <span>校园地址：XX大学XX校区</span>
            </li>
            <li class="contact-item">
              <i class="el-icon-phone"></i>
              <span>联系电话：123-4567-8910</span>
            </li>
            <li class="contact-item">
              <i class="el-icon-message"></i>
              <span>邮箱：contact@campustrading.com</span>
            </li>
            <li class="contact-item">
              <i class="el-icon-service"></i>
              <span>工作时间：周一至周日 9:00-22:00</span>
            </li>
          </ul>
        </div>
      </div>
      
      <!-- 页脚底部 -->
      <div class="footer-bottom">
        <div class="footer-copyright">
          © 2023 校园二手交易平台 版权所有 | 备案号：粤ICP备XXXXXXXX号
        </div>
        <div class="footer-links-bottom">
          <a href="#" class="link-item">隐私政策</a>
          <span class="separator">|</span>
          <a href="#" class="link-item">用户协议</a>
          <span class="separator">|</span>
          <a href="#" class="link-item">免责声明</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';

// 组件挂载时的处理
onMounted(() => {
  // 可以在这里添加一些初始化逻辑
});
</script>

<style lang="scss" scoped>
.footer {
  background-color: #2c3e50;
  color: #ecf0f1;
  padding: 40px 0 20px;
  margin-top: auto;
}

.footer-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  margin-bottom: 30px;
}

.footer-about,
.footer-links,
.footer-help,
.footer-contact {
  flex: 1;
  min-width: 200px;
  margin-bottom: 20px;
  padding: 0 10px;
}

.footer-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #fff;
  position: relative;
  padding-bottom: 10px;
}

.footer-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 40px;
  height: 2px;
  background-color: #3498db;
}

.footer-description {
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 15px;
  color: #bdc3c7;
}

.footer-social {
  display: flex;
}

.social-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  margin-right: 10px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.1);
  color: #ecf0f1;
  text-decoration: none;
  transition: all 0.3s;
}

.social-link:hover {
  background-color: #3498db;
  transform: translateY(-3px);
}

.link-list,
.contact-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.link-item {
  display: block;
  padding: 8px 0;
  color: #bdc3c7;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}

.link-item:hover {
  color: #3498db;
  padding-left: 5px;
}

.contact-item {
  display: flex;
  align-items: center;
  padding: 8px 0;
  font-size: 14px;
  color: #bdc3c7;
}

.contact-item i {
  margin-right: 10px;
  color: #3498db;
  width: 20px;
  text-align: center;
}

.footer-bottom {
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
}

.footer-copyright {
  font-size: 14px;
  color: #95a5a6;
  margin-bottom: 10px;
}

.footer-links-bottom {
  font-size: 12px;
  color: #95a5a6;
}

.footer-links-bottom .link-item {
  display: inline-block;
  padding: 0 10px;
  color: #95a5a6;
}

.footer-links-bottom .link-item:hover {
  color: #3498db;
  padding-left: 10px;
}

.separator {
  margin: 0 5px;
  color: #95a5a6;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .footer {
    padding: 30px 0 15px;
  }
  
  .footer-content {
    flex-direction: column;
  }
  
  .footer-about,
  .footer-links,
  .footer-help,
  .footer-contact {
    min-width: 100%;
    margin-bottom: 25px;
  }
  
  .footer-title {
    font-size: 16px;
  }
  
  .footer-description,
  .link-item,
  .contact-item,
  .footer-copyright {
    font-size: 13px;
  }
  
  .footer-links-bottom {
    font-size: 11px;
  }
}

@media (max-width: 480px) {
  .footer-container {
    padding: 0 15px;
  }
  
  .footer {
    padding: 20px 0 10px;
  }
  
  .footer-content {
    margin-bottom: 20px;
  }
  
  .footer-title {
    font-size: 15px;
    margin-bottom: 12px;
    padding-bottom: 8px;
  }
  
  .footer-title::after {
    width: 30px;
  }
  
  .footer-links-bottom .link-item {
    padding: 0 5px;
  }
}

/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.footer-content > div {
  animation: fadeInUp 0.6s ease-out;
}

.footer-about {
  animation-delay: 0.1s;
}

.footer-links {
  animation-delay: 0.2s;
}

.footer-help {
  animation-delay: 0.3s;
}

.footer-contact {
  animation-delay: 0.4s;
}

.footer-bottom {
  animation: fadeInUp 0.6s ease-out 0.5s;
}
</style>