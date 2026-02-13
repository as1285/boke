/**
 * Flask博客系统 - 主JavaScript文件
 * 包含常用的交互功能
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // 自动隐藏消息提示
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        }, 5000); // 5秒后自动关闭
    });
    
    // 确认删除操作
    const deleteForms = document.querySelectorAll('form[onsubmit*="confirm"]');
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const message = form.getAttribute('onsubmit').match(/confirm\('([^']+)'\)/);
            if (message && !confirm(message[1])) {
                e.preventDefault();
            }
        });
    });
    
    // 图片加载失败处理
    const images = document.querySelectorAll('img');
    images.forEach(function(img) {
        img.addEventListener('error', function() {
            // 如果图片加载失败，使用默认图片
            if (!img.src.includes('default_avatar.png')) {
                img.src = '/static/uploads/default_avatar.png';
            }
        });
    });
    
    // 搜索框焦点效果
    const searchInput = document.querySelector('input[type="search"]');
    if (searchInput) {
        searchInput.addEventListener('focus', function() {
            this.parentElement.classList.add('search-focused');
        });
        searchInput.addEventListener('blur', function() {
            this.parentElement.classList.remove('search-focused');
        });
    }
    
    // 文章编辑器自动保存草稿（如果页面有编辑器）
    const contentEditor = document.querySelector('textarea[name="content"]');
    if (contentEditor) {
        let autoSaveTimer;
        contentEditor.addEventListener('input', function() {
            clearTimeout(autoSaveTimer);
            autoSaveTimer = setTimeout(function() {
                // 这里可以实现自动保存逻辑
                console.log('草稿已自动保存');
            }, 30000); // 30秒后自动保存
        });
    }
    
    // 分页链接保持搜索参数
    const paginationLinks = document.querySelectorAll('.pagination a');
    const urlParams = new URLSearchParams(window.location.search);
    const keyword = urlParams.get('keyword');
    
    if (keyword) {
        paginationLinks.forEach(function(link) {
            const href = new URL(link.href);
            href.searchParams.set('keyword', keyword);
            link.href = href.toString();
        });
    }
    
    // 移动端菜单自动关闭
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            if (window.innerWidth < 992 && navbarCollapse.classList.contains('show')) {
                const toggleBtn = document.querySelector('.navbar-toggler');
                if (toggleBtn) {
                    toggleBtn.click();
                }
            }
        });
    });
    
    // 表格行悬停效果
    const tableRows = document.querySelectorAll('.table tbody tr');
    tableRows.forEach(function(row) {
        row.addEventListener('mouseenter', function() {
            this.classList.add('table-active');
        });
        row.addEventListener('mouseleave', function() {
            this.classList.remove('table-active');
        });
    });
    
    // 表单验证提示
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    
                    // 创建错误提示
                    let feedback = field.nextElementSibling;
                    if (!feedback || !feedback.classList.contains('invalid-feedback')) {
                        feedback = document.createElement('div');
                        feedback.className = 'invalid-feedback';
                        field.parentNode.insertBefore(feedback, field.nextSibling);
                    }
                    feedback.textContent = '此字段不能为空';
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
    
    // 清除表单验证错误
    const formInputs = document.querySelectorAll('.form-control');
    formInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            this.classList.remove('is-invalid');
        });
    });
    
    // 返回顶部按钮
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
    backToTopBtn.className = 'btn btn-primary btn-sm back-to-top';
    backToTopBtn.style.cssText = 'position: fixed; bottom: 20px; right: 20px; display: none; z-index: 1000; border-radius: 50%; width: 40px; height: 40px; padding: 0;';
    document.body.appendChild(backToTopBtn);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });
    
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // 代码块复制功能
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(function(block) {
        const copyBtn = document.createElement('button');
        copyBtn.className = 'btn btn-sm btn-outline-secondary copy-code-btn';
        copyBtn.innerHTML = '<i class="bi bi-clipboard"></i>';
        copyBtn.style.cssText = 'position: absolute; top: 5px; right: 5px; opacity: 0; transition: opacity 0.2s;';
        
        const pre = block.parentElement;
        pre.style.position = 'relative';
        pre.appendChild(copyBtn);
        
        pre.addEventListener('mouseenter', function() {
            copyBtn.style.opacity = '1';
        });
        pre.addEventListener('mouseleave', function() {
            copyBtn.style.opacity = '0';
        });
        
        copyBtn.addEventListener('click', function() {
            const code = block.textContent;
            navigator.clipboard.writeText(code).then(function() {
                copyBtn.innerHTML = '<i class="bi bi-check"></i>';
                setTimeout(function() {
                    copyBtn.innerHTML = '<i class="bi bi-clipboard"></i>';
                }, 2000);
            });
        });
    });
    
    console.log('Flask博客系统已加载完成');
});
