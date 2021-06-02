/*

Data object & functions to be used by Alpine.js x-data in training.html

*/

function trainingData() {
  return {
    /*
    Variables
    */
    selectedCert: '',
    selectedBadge: '',
    badgeList: [],
    visibleFlagList: [],
    completedFlags: 0,
    completedBadges: 0,
    flagList: [],
    completedCertificate: false,
    certificateCode: '',
    refresher: null,
    resetData() {
      this.badgeList = [];
      this.completedFlags = 0;
      this.completedBadges = 0;
      this.flagList = [];
    },

    /*
    onSelectBadge() is called by $watch in training.html, when the
    variable selectedBadge is updated,
    and updates the list of visible flags as well
    */
    onSelectBadge(badge = this.selectedBadge) {
      if (badge) {
        this.selectedBadge = badge;
        this.visibleFlagList = this.flagList.filter(
          (flag) => flag.badge_name === this.selectedBadge.name,
        );
      } else this.visibleFlagList = this.flagList;
    },

    /*
    Check if certificate is complete, and generate code if completed
    */
    checkCertificateCompletion(certificateCodeList) {
      if (this.completedBadges === this.badgeList.length) {
        this.completedCertificate = true;
        let code = certificateCodeList.sort((a, b) => a.toString().length - b.toString().length);
        code = code.join(' ');
        this.certificateCode = btoa(code);
      }
    },

    async getFlags(data) {
      if (!data) return;
      const certificateCodeList = [];
      this.resetData();

      // Fetch flag from API and compares it to previous data,
      // rather than completely override (for variables like showMore)
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

      this.checkCertificateCompletion(certificateCodeList);
      this.onSelectBadge();
    },

    /*
    getTraining() makes call to get flags, and if successful, sets a refresher() to
    fetch flags again after set interval
    */
    getTraining(selectedCert) {
      if (this.refresher) clearInterval(this.refresher);
      this.selectedCert = selectedCert;
      fetch('/plugin/training/flags', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: this.selectedCert, answers: {}
        }),
      })
        .then((r) => {
          if (r.ok) return r.json();
          return console.error('Fetch error:', r);
        }).then((data) => {
          this.getFlags(data).then(() => {
            this.refresher = setInterval(() => this.getTraining(this.selectedCert), 15000);
          });
          return true;
        }).catch((e) => console.error(e));
    },
  };
}
