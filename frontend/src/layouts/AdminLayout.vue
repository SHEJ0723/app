<template>
  <el-container class="admin-layout">
    <el-aside width="200px" v-show="!isMobile" class="sidebar">
      <el-menu
        :default-active="$route.path"
        router
        class="admin-menu"
      >
        <el-menu-item index="/admin/dashboard">
          <el-icon><Monitor /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/admin/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/parking">
          <el-icon><Location /></el-icon>
          <span>停车场管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/orders">
          <el-icon><List /></el-icon>
          <span>订单管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/assistant">
          <el-icon><ChatDotRound /></el-icon>
          <span>管理助手</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header height="60px">
        <div class="header-content">
          <h2>智慧停车场管理系统</h2>
          <el-dropdown>
            <span class="admin-info">
              管理员 <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main-gradient-bg">
        <router-view></router-view>
      </el-main>
    </el-container>
    <BottomNavAdmin />
  </el-container>
</template>

<script>
import { Monitor, User, Location, List, ArrowDown, ChatDotRound } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import BottomNavAdmin from '@/components/BottomNavAdmin.vue'

export default {
  name: 'AdminLayout',
  
  components: {
    Monitor,
    User,
    Location,
    List,
    ArrowDown,
    ChatDotRound,
    BottomNavAdmin
  },
  
  setup() {
    const router = useRouter()
    const isMobile = ref(window.innerWidth < 600)
    onMounted(() => {
      window.addEventListener('resize', () => {
        isMobile.value = window.innerWidth < 600
      })
    })
    
    const handleLogout = () => {
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      localStorage.removeItem('userType')
      router.push('/login')
    }
    
    return {
      handleLogout,
      isMobile
    }
  }
}
</script>

<style scoped>
.admin-layout {
  height: 100vh;
  min-height: 100vh;
  display: flex;
  flex-direction: row;
  background: #f5f7fa;
}

.admin-menu {
  height: 100%;
  border-right: none;
}

.el-header {
  background-color: white;
  border-bottom: 1px solid #e6e6e6;
  padding: 0 20px;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.admin-info {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.el-main {
  background-color: #f5f7fa;
  padding: 20px;
  flex: 1 1 0;
  min-width: 0;
  min-height: 0;
  overflow: auto;
  display: flex;
  flex-direction: column;
}

.sidebar, .el-aside.sidebar {
  background: linear-gradient(180deg, #a1c4fd 0%, #bbf7d0 40%, #7c3aed 100%) !important;
  min-height: 100vh !important;
  height: 100vh !important;
  box-shadow: 2px 0 8px rgba(80,80,160,0.04);
  border-top-right-radius: 24px;
  border-bottom-right-radius: 24px;
  position: relative;
  z-index: 2;
  transition: background 0.3s;
  display: flex;
  flex-direction: column;
}
.sidebar .el-menu, .el-aside.sidebar .el-menu {
  background: transparent !important;
  box-shadow: none !important;
  height: 100vh !important;
}
.sidebar::before, .el-aside.sidebar::before {
  content: '';
  position: absolute;
  top: 20px; left: 30px;
  width: 80px; height: 80px;
  background: radial-gradient(circle, #a1c4fd55 0%, #f0f9ff00 80%);
  border-radius: 50%;
  z-index: 0;
  pointer-events: none;
}
.main-gradient-bg, .el-main.main-gradient-bg {
  background: linear-gradient(120deg, #f0f9ff 60%, #e0e7ff 90%, #a1c4fd 100%) !important;
  min-height: 100vh !important;
  padding: 32px 0;
  position: relative;
}
.main-gradient-bg::before, .el-main.main-gradient-bg::before {
  content: '';
  position: absolute;
  right: 60px; bottom: 60px;
  width: 180px; height: 180px;
  background: radial-gradient(circle, #a1c4fd33 0%, #f0f9ff00 80%);
  border-radius: 50%;
  z-index: 0;
  pointer-events: none;
}

@media (max-width: 900px) {
  .admin-layout {
    flex-direction: column;
  }
  .el-aside {
    width: 100vw !important;
    min-width: 0 !important;
    max-width: 100vw !important;
    border-right: none;
  }
  .el-main {
    padding: 8px;
  }
}

@media (max-width: 600px) {
  .admin-layout {
    flex-direction: column;
    min-height: 100vh;
  }
  .el-header {
    padding: 0 6px;
    min-height: 48px;
    font-size: 16px;
  }
  .el-main {
    padding: 2px;
  }
}
</style> 