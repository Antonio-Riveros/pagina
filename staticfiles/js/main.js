document.addEventListener('DOMContentLoaded', () => {
    // Modal logic
    const modals = document.querySelectorAll('.modal-overlay');
    const modalTriggers = document.querySelectorAll('[data-modal-target]');
    const modalCloses = document.querySelectorAll('.modal-close, [data-modal-close]');

    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = trigger.getAttribute('data-modal-target');
            const targetModal = document.getElementById(targetId);
            
            if (targetModal) {
                // If it's a video modal, set the iframe src dynamically to auto-play if needed
                const iframe = targetModal.querySelector('iframe');
                if (iframe && iframe.dataset.src) {
                    iframe.src = iframe.dataset.src;
                }
                
                targetModal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        });
    });

    const closeModal = (modal) => {
        modal.classList.remove('active');
        document.body.style.overflow = '';
        
        // Stop video playback if it's a video modal
        const iframe = modal.querySelector('iframe');
        if (iframe) {
            iframe.src = '';
        }
    };

    modalCloses.forEach(closeBtn => {
        closeBtn.addEventListener('click', () => {
            const modal = closeBtn.closest('.modal-overlay');
            if (modal) {
                closeModal(modal);
            }
        });
    });

    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal(modal);
            }
        });
    });

    // Close on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const activeModal = document.querySelector('.modal-overlay.active');
            if (activeModal) {
                closeModal(activeModal);
            }
        }
    });
});
