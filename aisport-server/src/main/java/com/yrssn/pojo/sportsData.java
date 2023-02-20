package com.yrssn.pojo;

import com.baomidou.mybatisplus.annotation.TableId;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.sql.Time;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class sportsData {
    @TableId
    private Integer sid;
    private String suid;
    private String stime;
    private String sname;
    private Integer scount;
    private Integer sscore;
    private Integer syundongtime;

}
