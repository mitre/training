function trainingData() {
    return {
        selectedCert: '',
        selectedBadge: '',
        badgeList: [],
        completedBadges: 0,
        flagList: [],
        completedFlags: 0,
        resetData() {
            this.badgeList = [];
            this.flagList = [];
            this.completedFlags = 0;
            this.completedBadges = 0;
            this.completedCertificate = false;
            this.certificateCode = '';
        },
        getFlags(data) {
            if (!data) return;
            this.resetData();
            let certificateCodeList = [];

            data.badges.forEach((badge) => {
                console.log('BADGE', badge.name)
                let iconSrc = `/training/img/badges/${badge.name}.png`;
                let isBadgeCompleted = false;
                let badgeCompletedFlags = 0;
                badge.flags.forEach((flag) => {
                    if (flag.completed) badgeCompletedFlags += 1;
                    this.flagList.push({
                        ...flag,
                        badge_name: badge.name,
                        badge_icon: iconSrc,
                        cert_name: this.selectedCert
                    });
                    certificateCodeList.push(flag.code);
                });

                if (badgeCompletedFlags === badge.flags.length) {
                    this.completedBadges += 1;
                    isBadgeCompleted = true;
                }

                this.badgeList.push({...badge, completed: isBadgeCompleted, icon_src: iconSrc});
                this.completedFlags += badgeCompletedFlags;
            });

            if (this.completedBadges === this.badgeList.length) {
                this.completedCertificate = true;
                this.certificateCode = this.getCertificateCode(certificateCodeList);
            }
            this.visibleFlagList = this.flagList;
            console.log('COMPLETED GET FLAGS', this.badgeList)
        },
        getTraining(selectedCert) {
            this.selectedCert = selectedCert;
            console.log('ELLO', this.selectedCert)
            fetch('/plugin/training/flags', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({name: this.selectedCert, answers: {}}),
            }).then(r => {
                if (r.ok) return r.json(); else console.error('Fetch error:', r)
            }).then((data) => {
                console.log('success', data);
                this.getFlags(data);
                return true;
            }).catch(e => console.error(e));
        }
    }
}
