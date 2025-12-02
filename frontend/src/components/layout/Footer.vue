<template>
  <footer class="footer">
    <div class="footer-container">
      <!-- 页脚内容区域 -->
      <div class="footer-content">
        <!-- 网站介绍 -->
        <div class="footer-about">
          <h3 class="footer-title">{{ $t('footer.about') }}</h3>
          <p class="footer-description">
            {{ $t('footer.aboutDesc') }}
          </p>
          <div class="footer-social">
            <a href="#" class="social-link" title="WeChat"><el-icon><ChatLineSquare /></el-icon></a>
            <a href="#" class="social-link" title="QQ"><el-icon><ChatDotRound /></el-icon></a>
            <a href="#" class="social-link" title="Weibo"><el-icon><Share /></el-icon></a>
          </div>
        </div>

        <!-- 快速链接 -->
        <div class="footer-links">
          <h3 class="footer-title">{{ $t('footer.quickLinks') }}</h3>
          <ul class="link-list">
            <li><router-link to="/" class="link-item">{{ $t('nav.home') }}</router-link></li>
            <li><router-link to="/items" class="link-item">{{ $t('nav.items') }}</router-link></li>
            <li><router-link to="/requests" class="link-item">{{ $t('nav.requests') }}</router-link></li>
            <li><router-link to="/compare" class="link-item">{{ $t('nav.compare') }}</router-link></li>
            <li><router-link to="/about" class="link-item">{{ $t('nav.about') }}</router-link></li>
          </ul>
        </div>

        <!-- 帮助中心 -->
        <div class="footer-help">
          <h3 class="footer-title">{{ $t('footer.helpCenter') }}</h3>
          <ul class="link-list">
            <li><a href="#" class="link-item">{{ $t('footer.newbieGuide') }}</a></li>
            <li><a href="#" class="link-item">{{ $t('footer.tradingRules') }}</a></li>
            <li><a href="#" class="link-item">{{ $t('footer.faq') }}</a></li>
            <li><a href="#" class="link-item">{{ $t('footer.feedback') }}</a></li>
            <li><a href="#" class="link-item">{{ $t('footer.customerService') }}</a></li>
          </ul>
        </div>

        <!-- 联系我们 -->
        <div class="footer-contact">
          <h3 class="footer-title">{{ $t('footer.contactUs') }}</h3>
          <ul class="contact-list">
            <li class="contact-item">
              <el-icon><Location /></el-icon>
              <span>{{ $t('footer.address') }}</span>
            </li>
            <li class="contact-item">
              <el-icon><Phone /></el-icon>
              <span>{{ $t('footer.phone') }}</span>
            </li>
            <li class="contact-item">
              <el-icon><Message /></el-icon>
              <span>{{ $t('footer.email') }}</span>
            </li>
            <li class="contact-item">
              <el-icon><Service /></el-icon>
              <span>{{ $t('footer.workTime') }}</span>
            </li>
          </ul>
        </div>
      </div>

      <!-- 页脚底部 -->
      <div class="footer-bottom">
        <div class="footer-copyright">
          {{ $t('footer.copyright') }}
        </div>
        <div class="footer-links-bottom">
          <a href="#" class="link-item">{{ $t('footer.privacyPolicy') }}</a>
          <span class="separator">|</span>
          <a href="#" class="link-item">{{ $t('footer.userAgreement') }}</a>
          <span class="separator">|</span>
          <a href="#" class="link-item">{{ $t('footer.disclaimer') }}</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import {
  ChatLineSquare,
  ChatDotRound,
  Share,
  Location,
  Phone,
  Message,
  Service
} from '@element-plus/icons-vue';
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