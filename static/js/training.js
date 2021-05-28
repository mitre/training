function trainingData() {
  return {
    selectedCert: '',
    selectedBadge: '',
    badgeList: [],
    visibleFlagList: [],
    completedFlags: 0,
    completedBadges: 0,
    visibleFlagList: [],
    flagList: [],
    completedCertificate: false,
    certificateCode: '',
    refresher: null,
    resetData() {
      this.badgeList = [];
      this.visibleFlagList = [];
      this.completedFlags = 0;
      this.completedBadges = 0;
      this.flagList = [];
      this.visibleFlagList = [];
    },
    onSelectBadge(badge) {
      if (badge) {
        this.selectedBadge = badge;
        this.visibleFlagList = this.flagList.filter(
          (flag) => flag.badge_name === this.selectedBadge.name,
        );
      } else this.visibleFlagList = this.flagList;
    },
    getCertificateCode(certificateCodeList) {
        let code = certificateCodeList.sort((a, b) => a.toString().length - b.toString().length);
        code = code.join(' ');
        return btoa(code);
    },
    getFlags(data) {
      if (!data) return;
      this.resetData();
      const certificateCodeList = [];

      data.badges.forEach((badge) => {
        const iconSrc = `/training/img/badges/${badge.name}.png`;
        let isBadgeCompleted = false;
        let badgeCompletedFlags = 0;
        badge.flags.forEach((flag) => {
          if (flag.completed) badgeCompletedFlags += 1;
          this.flagList.push({
            ...flag,
            badge_name: badge.name,
            badge_icon: iconSrc,
            cert_name: this.selectedCert,
            showMore: false,
          });
          certificateCodeList.push(flag.code);
        });

        if (badgeCompletedFlags === badge.flags.length) {
          this.completedBadges += 1;
          isBadgeCompleted = true;
        }

        this.badgeList.push({ ...badge, completed: isBadgeCompleted, icon_src: iconSrc });
        this.completedFlags += badgeCompletedFlags;
      });

      if (this.completedBadges === this.badgeList.length) {
        this.completedCertificate = true;
        this.certificateCode = this.getCertificateCode(certificateCodeList);
      }
      this.visibleFlagList = this.flagList;
    },
    getTraining(selectedCert) {
      this.selectedCert = selectedCert;
      fetch('/plugin/training/flags', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: this.selectedCert, answers: {} }),
      }).then((r) => {
        if (r.ok) return r.json();
        return console.error('Fetch error:', r);
      }).then((data) => {
        this.getFlags(data);
        return true;
      }).catch((e) => console.error(e));
    },
  };
}
